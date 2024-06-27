package ifneeded example 1.0.0

namespace eval ::ttk::theme::example {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create example -parent default -settings {
            ttk::style configure TButton -background #9b59b6 -foreground #ffffff -font {Arial 10 bold} -padding {8 12} -borderwidth 0 -borderradius 5
            ttk::style map TButton -background [list active #8e44ad]
            ttk::style configure TLabel -foreground #333333 -font {Arial 10 bold}
            ttk::style configure TEntry -background #d1c4e9 -foreground #333333 -font {Arial 10} -padding 5 -borderwidth 1 -relief solid
            ttk::style configure TText -background #d1c4e9 -foreground #333333 -font {Arial 10} -padding 5 -borderwidth 1 -relief solid
            ttk::style configure TFrame -background #d1c4e9 -borderwidth 0
        }
    }
}

if {[info commands ::ttk::theme::example::Theme] ne ""} {
    ::ttk::theme::example::Theme
}
