package ifneeded azure-dark 1.0.0

namespace eval ::ttk::theme::azure-dark {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create azure-dark -parent default -settings {
            ttk::style configure TButton -background #3498db -foreground #ffffff -font {Arial 10} -padding {5 10}
            ttk::style configure TLabel -foreground #333333 -font {Arial 10 bold}
            ttk::style configure TEntry -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5
            ttk::style configure TText -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5
            ttk::style configure TFrame -background #ecf0f1
        }
    }
}

if {[info commands ::ttk::theme::azure-dark::Theme] ne ""} {
    ::ttk::theme::azure-dark::Theme
}
