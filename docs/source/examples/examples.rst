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
.. highlight:: none

Example: theme configuration
----------------------------

This is how a theme configuration file may look like 
(using the `Dracula theme`_ [#f1]_ as an example):

`theme.toml`::

    name = "Dracula"
    
    
    [[installation_check]]
    required_by = "Xresources"
    type = "file_exists"
    file = "%D/Xresources"

    [[installation_check]]
    required_by = "Visual Studio Code"
    type = "json_entry"
    file = "~/.vscode/extensions/extensions.json"
    json_entry = [
        "?",
        "identifier",
        "id"
    ]
    value = "dracula-theme.theme-dracula"


    [[applications]]
    id = "Xresources"
    
    [applications.procedure]
    id = "merge"
    file = "%D/Xresources"

    [[applications]]
    id = "Visual Studio Code"

    [applications.procedure]
    id = "user_config_theme"
    theme_name = "Dracula"

An equivalent configuration written in `JSON` would look like this::

    sus

.. _examples_application_configuration:

Example: application configuration
----------------------------------

This example is one of the default configuration shipped with the program.

`vscode.toml`::

    [id]
    desktop_entry = "/usr/share/applications/code.desktop"
    name = "Visual Studio Code"


    [[installation_check]]
    type = "which"
    command = "code"


    [[apply_procedures]]
    id = "user_config_theme"

    [[apply_procedures.requires]]
    id = "theme_name"
    type = "string"

    [apply_procedures.function]
    type = "json_entry"
    file = "~/.config/Code/User/settings.json"
    json_entry = [
        "workbench.colorTheme"
    ]
    value = "%theme_name"

An equivalent configuration written in `JSON` would look like this::

    sus

.. rubric:: Footnotes
.. [#f1] `Dracula theme`_: (`https://draculatheme.com/ <Dracula theme>`_)

.. _`Dracula theme`: https://draculatheme.com/