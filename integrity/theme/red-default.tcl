package ifneeded red-default 1.0.0

namespace eval ::ttk::theme::red-default {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create red-default -parent default -settings {
            ttk::style configure TButton -background #e74c3c -foreground #ffffff -font {Arial 10 bold} -padding {8 12} -borderwidth 0 -borderradius 5
            ttk::style map TButton -background [list active #c0392b]
            ttk::style configure TLabel -foreground #333333 -font {Arial 10 bold}
            ttk::style configure TEntry -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5 -borderwidth 1 -relief solid
            ttk::style configure TText -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5 -borderwidth 1 -relief solid
            ttk::style configure TFrame -background #ecf0f1 -borderwidth 0
        }
    }
}

if {[info commands ::ttk::theme::red-default::Theme] ne ""} {
    ::ttk::theme::red-default::Theme
}
