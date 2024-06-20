package ifneeded azure-default 1.0.0

namespace eval ::ttk::theme::azure-default {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create azure-default -parent default -settings {
            ttk::style configure TButton -background #3498db -foreground #ffffff -font {Arial 10 bold} -padding {8 12} -borderwidth 2 -relief groove
            ttk::style map TButton -background [list active #2980b9]
            ttk::style configure TLabel -foreground #333333 -font {Arial 10 bold}
            ttk::style configure TEntry -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5 -borderwidth 1 -relief solid
            ttk::style configure TText -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5 -borderwidth 1 -relief solid
            ttk::style configure TFrame -background #ecf0f1 -borderwidth 0
        }
    }
}

if {[info commands ::ttk::theme::azure-default::Theme] ne ""} {
    ::ttk::theme::azure-default::Theme
}
