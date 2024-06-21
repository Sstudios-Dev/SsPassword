import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pygments import lex
from pygments.lexers import TclLexer
from pygments.styles import get_style_by_name
import os

class LineNumberCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_widget = None

    def attach(self, text_widget):
        self.text_widget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, font=("Courier New", 12))
            i = self.text_widget.index(f"{i}+1line")

class TclEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Tcl Template Editor")
        self.root.geometry("800x600")

        self.create_menu()
        self.create_text_widget()
        self.current_file = None
        self.setup_autocomplete()
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Escape>", lambda event: self.root.quit())

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        self.root.config(menu=menubar)
        
    def create_text_widget(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=1)

        self.line_numbers = LineNumberCanvas(self.text_frame, width=40)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_area = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, font=("Courier New", 12))
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.text_area.bind("<KeyPress>", self.on_key_press)

        self.line_numbers.attach(self.text_area)

        self.text_area.bind("<MouseWheel>", self.on_scroll)
        self.text_area.bind("<Button-4>", self.on_scroll)
        self.text_area.bind("<Button-5>", self.on_scroll)

    def setup_autocomplete(self):
        self.autocomplete_words = ['proc', 'set', 'if', 'else', 'foreach', 'while', 'expr', 'return', 'puts', 'list', 'array', 'namespace']
        self.autocomplete_listbox = None

    def on_key_release(self, event):
        self.highlight_syntax()
        self.line_numbers.redraw()
        if event.keysym in ('BackSpace', 'Delete'):
            self.hide_autocomplete()
        elif event.keysym.isalpha():
            self.show_autocomplete()

    def on_key_press(self, event):
        if event.keysym == "Tab":
            self.text_area.insert(tk.INSERT, " " * 4)
            return "break"
        if self.autocomplete_listbox:
            if event.keysym in ('Return', 'Tab'):
                self.insert_autocomplete()
                return 'break'
            elif event.keysym == 'Escape':
                self.hide_autocomplete()

    def on_scroll(self, event):
        self.line_numbers.redraw()

    def show_autocomplete(self):
        current_word = self.get_current_word()
        if not current_word:
            self.hide_autocomplete()
            return
        
        matches = [w for w in self.autocomplete_words if w.startswith(current_word)]
        if not matches:
            self.hide_autocomplete()
            return

        if not self.autocomplete_listbox:
            self.create_autocomplete_listbox()

        self.update_autocomplete_listbox(matches)

    def create_autocomplete_listbox(self):
        self.autocomplete_listbox = tk.Listbox(self.root, font=("Courier New", 12), height=5)
        self.autocomplete_listbox.bind("<Button-1>", lambda event: self.insert_autocomplete())
        self.autocomplete_listbox.place(x=0, y=0)
        self.autocomplete_listbox.lift()

    def update_autocomplete_listbox(self, matches):
        self.autocomplete_listbox.delete(0, tk.END)
        for match in matches:
            self.autocomplete_listbox.insert(tk.END, match)

        self.position_autocomplete_listbox()

    def position_autocomplete_listbox(self):
        cursor_position = self.text_area.index(tk.INSERT)
        x, y, _, _ = self.text_area.bbox(cursor_position)
        self.autocomplete_listbox.place(x=x, y=y + 30)

    def insert_autocomplete(self):
        if not self.autocomplete_listbox:
            return

        current_word = self.get_current_word()
        selected_word = self.autocomplete_listbox.get(tk.ACTIVE)
        if current_word and selected_word:
            self.text_area.delete(f"insert-{len(current_word)}c", tk.INSERT)
            self.text_area.insert(tk.INSERT, selected_word)
        self.hide_autocomplete()

    def hide_autocomplete(self):
        if self.autocomplete_listbox:
            self.autocomplete_listbox.destroy()
            self.autocomplete_listbox = None

    def get_current_word(self):
        cursor_position = self.text_area.index(tk.INSERT)
        line_start = f"{cursor_position.split('.')[0]}.0"
        line_text = self.text_area.get(line_start, cursor_position)
        return line_text.split()[-1] if line_text.split() else ""

    def highlight_syntax(self):
        content = self.text_area.get("1.0", tk.END)
        self.text_area.mark_set("range_start", "1.0")
        
        for token, content in lex(content, TclLexer()):
            self.text_area.mark_set("range_end", f"{self.text_area.index('range_start')}+{len(content)}c")
            self.text_area.tag_add(str(token), "range_start", "range_end")
            self.text_area.mark_set("range_start", "range_end")
        
        style = get_style_by_name('default')
        for token, settings in style.styles.items():
            if settings:
                color = next((part for part in settings.split() if part.startswith('#')), None)
                if color:
                    self.text_area.tag_configure(str(token), foreground=color)

    def new_file(self):
        if self.confirm_save():
            self.text_area.delete(1.0, tk.END)
            self.root.title("Tcl Template Editor - New File")
            self.current_file = None
            
    def open_file(self):
        if self.confirm_save():
            try:
                file_path = filedialog.askopenfilename(defaultextension=".tcl", filetypes=[("Tcl Files", "*.tcl"), ("All Files", "*.*")])
                if file_path:
                    with open(file_path, "r") as file:
                        content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.root.title(f"Tcl Template Editor - {file_path}")
                    self.current_file = file_path
                    self.highlight_syntax()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while opening the file:\n{str(e)}")
                
    def save_file(self, event=None):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Save File", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file:\n{str(e)}")
        else:
            self.save_as_file()
            
    def save_as_file(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".tcl", filetypes=[("Tcl Files", "*.tcl"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.root.title(f"Tcl Template Editor - {file_path}")
                self.current_file = file_path
                messagebox.showinfo("Save File", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file:\n{str(e)}")
            
    def confirm_save(self):
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Save File", "Do you want to save changes to your current file?")
            if response:
                self.save_file()
                return True
            elif response is None:
                return False
        return True

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TclEditor(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running the application:\n{str(e)}")
