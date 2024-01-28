.. _examples_start:

Examples
========

.. _example_root_directory_file_tree:

Example: root directory file tree
---------------------------------

Considering the default values for the XDG configuration and data directories::
  
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
    ├─applications
    │ ├─incredible-application.toml
    │ ├─awesome-application.json
    │ └─...
    ├─themes
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
    ├─scripts
    │ ├─enabling_procedures
    │ │ ├─magic_enabling_procedure.py
    │ │ └─...
    │ ├─check_procedures
    │ │ ├─magic_check_procedure.py
    │ │ └─...
    │ ├─references
    │ │ ├─magic_reference.py
    │ │ └─...
    │ └─...
    └─...



.. _example_application_configuration:

Example: application configuration
----------------------------------

This example is one of the default configurations shipped with the program.

.. highlight:: toml

`Xresources.toml`::

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

.. highlight:: json

An equivalent configuration written in `JSON` would look like this::

    {
      "name": "Xresources",
      "check_procedures": [
        {
          "type": "command_exists",
          "command": "xrdb"
        }
      ],
      "enabling_procedures": [
        {
          "id": "replace",
          "requires": [
            {
              "id": "file",
              "type": "path"
            }
          ],
          "function": {
            "type": "shell",
            "command": "xrdb",
            "args": [
              "@file"
            ]
          }
        },
        {
          "id": "merge",
          "requires": [
            {
              "id": "file",
              "type": "path"
            }
          ],
          "function": {
            "type": "shell",
            "command": "xrdb",
            "args": [
              "-merge",
              "@file"
            ]
          }
        },
        {
          "id": "symlink",
          "requires": [
            {
              "id": "target",
              "type": "path"
            },
            {
              "id": "directory",
              "type": "path"
            }
          ],
          "function": {
            "type": "create_symlink",
            "target": "@target",
            "directory": "@directory"
          }
        }
      ]
    }

.. highlight:: none

If you want to see more examples, check the default configurations shipped 
with the program.

.. _example_theme_configuration:

Example: theme configuration
----------------------------

This is how a theme configuration file written in `TOML` may look like
(using a basic config for the `Dracula theme`_ as an example [#f1]_):

.. highlight:: toml

`theme.toml`::

    name = "Dracula"
    
    
    [[check_procedures]]
    required_by = "Xresources"
    type = "file_exists"
    file = "@THEME_DIR/Xresources"

    [[check_procedures]]
    required_by = "Visual Studio Code"
    type = "json_entry"
    file = "@HOME/.vscode/extensions/extensions.json"
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
    file = "@THEME_DIR/Xresources"

    [[applications]]
    id = "Visual Studio Code"

    [applications.procedure]
    id = "user_config_theme"
    theme_name = "Dracula"

.. highlight:: json

An equivalent configuration written in `JSON` would look like this::

    {
      "name": "Dracula",
      "check_procedures": [
        {
          "required_by": "Xresources",
          "type": "file_exists",
          "file": "@THEME_DIR/Xresources"
        },
        {
          "required_by": "Visual Studio Code",
          "type": "json_entry",
          "file": "@HOME/.vscode/extensions/extensions.json",
          "entry": [
            "?",
            "identifier",
            "id"
          ],
          "value": "dracula-theme.theme-dracula"
        }
      ],
      "applications": [
        {
          "id": "Xresources",
          "procedure": {
            "id": "merge",
            "file": "@THEME_DIR/Xresources"
          }
        },
        {
          "id": "Visual Studio Code",
          "procedure": {
            "id": "user_config_theme",
            "theme_name": "Dracula"
          }
        }
      ]
    }

.. highlight:: none

.. _example_script:

Example: script
---------------

This is how a simple script for may look like (exaple of a script for a reference):

.. highlight:: python

`get_api_key.py`::

    import os

    def main(logger):
        """Gets the API key from the environment variable API_KEY."""
        
        api_key = os.getenv('API_KEY')
        logger.debug(f'$API_KEY value: {api_key}.', __name__)

        if not api_key:
            return logger.error('The environment variable "API_KEY" doesn\'t exist.', 65, __name__)
        
        logger.info(f'Got the API key. ')

        return api_key

.. highlight:: none

.. rubric:: Footnotes
.. [#f1] `Dracula theme`_: (`https://draculatheme.com/ <Dracula theme>`_) 

.. _`Dracula theme`: https://draculatheme.com/