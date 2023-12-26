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
    │ │ ├─.config
    │ │ │ ├─theme-manager
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


.. _examples_application_configuration:
.. highlight:: none

Example: application configuration
----------------------------------

.. _examples_application_configuration_application_toml:

This example is one of the default configurations shipped with the program.

`vscode.toml`::

    [id]
    desktop_entry = "/usr/share/applications/code.desktop"
    name = "Visual Studio Code"


    [[installation_check]]
    type = "which"
    command = "code"


    [[enabling_procedures]]
    id = "user_config_theme"

    [[enabling_procedures.requires]]
    id = "theme_name"
    type = "string"

    [enabling_procedures.function]
    type = "json_entry"
    file = "@H/.config/Code/User/settings.json"
    json_entry = [
        "workbench.colorTheme"
    ]
    value = "@theme_name"

An equivalent configuration written in `JSON` would look like this::

    sus


.. _examples_theme_configuration:

Example: theme configuration
----------------------------

.. _examples_theme_configuration_theme_toml:

This is how a theme configuration file written in `TOML` may look like
(using a basic config for the `Dracula theme`_ as an example [#f1]_):

`theme.toml`::

    name = "Dracula"
    
    
    [[installation_check]]
    required_by = "Xresources"
    type = "file_exists"
    file = "@D/Xresources"

    [[installation_check]]
    required_by = "Visual Studio Code"
    type = "json_entry"
    file = "@H/.vscode/extensions/extensions.json"
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
    file = "@D/Xresources"

    [[applications]]
    id = "Visual Studio Code"

    [applications.procedure]
    id = "user_config_theme"
    theme_name = "Dracula"

An equivalent configuration written in `JSON` would look like this::

    sus

.. rubric:: Footnotes
.. [#f1] `Dracula theme`_: (`https://draculatheme.com/ <Dracula theme>`_) 

.. _`Dracula theme`: https://draculatheme.com/