package ifneeded modern-light 1.0.0

namespace eval ::ttk::theme::modern-light {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create modern-light -parent default -settings {
            ttk::style configure TButton -background #FF6F61 -foreground #FFFFFF -font {Arial 10} -padding {5 10}
            ttk::style configure TLabel -foreground #555555 -font {Arial 10 bold}
            ttk::style configure TEntry -background #F5F5F5 -foreground #555555 -font {Arial 10} -padding 5
            ttk::style configure TText -background #F5F5F5 -foreground #555555 -font {Arial 10} -padding 5
            ttk::style configure TFrame -background #FFFFFF

            # Style for when the mouse is over the button
            ttk::style map TButton -background [list active #E94E3E]
        }
    }
}

if {[info commands ::ttk::theme::modern-light::Theme] ne ""} {
    ::ttk::theme::modern-light::Theme
}
