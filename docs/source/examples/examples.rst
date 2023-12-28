.. _examples_start:

Examples
========

.. _example_root_directory_file_tree:

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

.. _example_theme_manager_file_tree:

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


.. highlight:: none

.. _example_application_configuration:

Example: application configuration
----------------------------------

This example is one of the default configurations shipped with the program.

`Xresources.toml`::

    [id]
    desktop_entry = false
    name = "Xresources"


    [[check_procedures]]
    type = "command_exists"
    command = "xrdb"


    [[enabling_procedures]]
    id = "replace"

    [[enabling_procedures.requires]]
    id = "file"
    type = "path"

    [enabling_procedures.function]
    type = "shell"
    command = "xrdb"
    args = [
        "@file"
    ]


    [[enabling_procedures]]
    id = "merge"

    [[enabling_procedures.requires]]
    id = "file"
    type = "path"

    [enabling_procedures.function]
    type = "shell"
    command = "xrdb"
    args = [
        "-merge",
        "@file"
    ]


    [[enabling_procedures]]
    id = "symlink"

    [[enabling_procedures.requires]]
    id = "target"
    type = "path"

    [[enabling_procedures.requires]]
    id = "directory"
    type = "path"

    [enabling_procedures.function]
    type = "create_symlink"
    target = "@target"
    directory = "@directory"

An equivalent configuration written in `JSON` would look like this::

    sus

If you want to see more examples, check the default configurations shipped 
with the program.

.. _example_theme_configuration:

Example: theme configuration
----------------------------

This is how a theme configuration file written in `TOML` may look like
(using a basic config for the `Dracula theme`_ as an example [#f1]_):

`theme.toml`::

    name = "Dracula"
    
    
    [[check_procedures]]
    required_by = "Xresources"
    type = "file_exists"
    file = "@D/Xresources"

    [[check_procedures]]
    required_by = "Visual Studio Code"
    type = "json_entry"
    file = "@H/.vscode/extensions/extensions.json"
    entry = [
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