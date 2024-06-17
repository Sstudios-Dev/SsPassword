package ifneeded azure-dark 1.0.0

namespace eval ::ttk::theme::azure-dark {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create azure-dark -parent default -settings {
            ttk::style configure TButton -background #2e2e2e -foreground #ffffff -font {Arial 10}
            ttk::style configure TLabel -background #2e2e2e -foreground #ffffff -font {Arial 10}
            ttk::style configure TEntry -background #2e2e2e -foreground #ffffff -font {Arial 10}
            ttk::style configure TText -background #2e2e2e -foreground #ffffff -font {Arial 10}
            ttk::style configure TFrame -background #2e2e2e -foreground #ffffff
        }
    }
}

if {[info commands ::ttk::theme::azure-dark::Theme] ne ""} {
    ::ttk::theme::azure-dark::Theme
}
