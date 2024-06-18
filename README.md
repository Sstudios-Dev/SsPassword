# SsPassword

## Installation

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Generate a secret key by executing:

```python
from app.encryption import generate_key, save_key
key = generate_key()
save_key(key)
```

# Customized theme

```tcl package ifneeded azure-default 1.0.0

namespace eval ::ttk::theme::azure-default {
    variable version 1.0.0

    proc Theme {} {
        ttk::style theme create azure-default -parent default -settings {
            ttk::style configure TButton -background #3498db -foreground #ffffff -font {Arial 10} -padding {5 10}
            ttk::style configure TLabel -foreground #333333 -font {Arial 10 bold}
            ttk::style configure TEntry -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5
            ttk::style configure TText -background #ecf0f1 -foreground #333333 -font {Arial 10} -padding 5
            ttk::style configure TFrame -background #ecf0f1

            # Style for when the mouse is over the button
            ttk::style map TButton -background [list active #2980b9]
        }
    }
}

if {[info commands ::ttk::theme::azure-default::Theme] ne ""} {
    ::ttk::theme::azure-default::Theme
} ```
