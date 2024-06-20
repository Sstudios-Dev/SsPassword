package ifneeded dark-default 1.0.0

namespace eval ::ttk::theme::dark-default {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create dark-default -parent default -settings {
            ttk::style configure TButton -background #4A4A4A -foreground #D8D8D8 -font {Arial 10 bold} -padding {6 12} -borderwidth 2 -relief raised
            ttk::style configure TButton.TButton:hover -background #5A5A5A

            ttk::style configure TLabel -foreground #B0B0B0 -font {Arial 10} -padding {3 0}
            ttk::style configure TEntry -background #2E2E2E -foreground #B0B0B0 -font {Arial 10} -padding {5 10} -borderwidth 1 -relief solid
            ttk::style configure TText -background #2E2E2E -foreground #B0B0B0 -font {Arial 10} -padding {5 10} -borderwidth 1 -relief solid
            ttk::style configure TFrame -background #1E1E1E

            ttk::style configure TScrollbar -background #2E2E2E -troughcolor #1E1E1E -borderwidth 0
            ttk::style configure TScrollbar.TScrollbar -background #4A4A4A -troughcolor #1E1E1E -borderwidth 0

            ttk::style configure TCombobox -fieldbackground #2E2E2E -foreground #B0B0B0 -background #2E2E2E -arrowcolor #B0B0B0 -font {Arial 10} -padding {5 10}

            # Style for when the mouse is over the button
            ttk::style map TButton -background [list active #5A5A5A]
        }
    }
}

if {[info commands ::ttk::theme::dark-default::Theme] ne ""} {
    ::ttk::theme::dark-default::Theme
}
