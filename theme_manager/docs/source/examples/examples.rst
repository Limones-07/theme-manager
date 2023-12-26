.. _examples_start:

Examples
========

.. _examples_root_directory_file_tree:

Example: root directory file tree
---------------------------------

Considering the default values for the XDG data directories::
  
    /
    ├─home
    │ ├─incredible-user
    │ │ ├─.local
    │ │ │ ├─share
    │ │ │ │ ├─theme-manager
    │ │ │ │ │ └─...
    │ │ │ │ └─...
    │ │ │ └─...
    │ │ └─...
    │ └─...
    ├─usr
    │ ├─local
    │ │ ├─share
    │ │ │ ├─theme-manager
    │ │ │ │ └─...
    │ │ │ └─...
    │ │ └─...
    │ ├─share
    │ │ ├─theme-manager
    │ │ │ └─...
    │ │ └─...
    │ └─...
    └─...

.. _examples_theme_manager_file_tree:

Example: `theme-manager` file tree
----------------------------------

This is how a generic `theme-manager` file tree should look like::

    theme-manager
    ├─theme-manager.toml
    ├─themes
    │ ├─themes.toml
    │ ├─incredible-theme
    │ │ ├─theme.toml
    │ │ ├─Xresources
    │ │ ├─LICENSE
    │ │ └─...
    │ ├─awesome-theme
    │ │ ├─theme.json
    │ │ ├─Xresources
    │ │ ├─bspwmrc
    │ │ ├─LICENSE
    │ │ └─...
    │ └─...
    ├─applications
    │ ├─incredible-application.toml
    │ ├─awesome-application.json
    │ └─...
    ├─scripts
    │ ├─magic_script.py
    │ └─...
    └─...

.. _examples_theme_configuration:

Example: theme configuration
----------------------------

This is how a theme configuration file may look like::

`theme.toml`::

    name = "Dracula"

    [[applications]]
    [applications.id]
    desktop_entry = null
    name = "Xresources"

    [[applications.installation_check]]
    type = "file_exists"
    file = "%d/Xresources"

    applications.application_args = []

    [[applications]]
    [applications.id]
    desktop_entry = "/usr/share/applications/code.desktop"
    name = "Visual Studio Code"

    [[applications.installation_check]]
    type = ""
    
    

An equivalent configuration written in `JSON` would look like this::

    same situation as toml lol

.. _examples_application_configuration:

Example: application configuration
----------------------------------

This example is one of the default configuration shipped with the program.

`dunno.json`::

    IF I DIDN'T DO THE THEME, WHAT MAKES YOU THINK I MADE THE APPLICATION?????

An equivalent configuration written in `TOML` would look like this::

    [id]
    desktop_entry = null
    name = "Visual Studio Code"
    
    
