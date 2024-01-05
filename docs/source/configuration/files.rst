.. _configuration_files_start:

Where to place directories and files
====================================

`theme-manager` looks for same named directories on the folders specified by the 
environment variables `$XDG_CONFIG_HOME` and `$XDG_DATA_DIRS` as defined by
the `XDG Base Directory Specification`_ [#f1]_. If the variables are not defined, 
`theme-manager` will look for its directories on `$HOME/.config`, `/usr/local/share` 
and `/usr/share`. 

This order is the order of priority, so, for example, if two configuration files 
are found with the **same name** at `$HOME/.config` and at `/usr/local/share`, 
the first one overrides the second. On the other hand, `theme-manager` will combine
what it finds in all three directories, allowing, for example, a theme configuration
on `/usr/share` to use an application configured at `$HOME/.config` and a script
at `/usr/local/share`.

User-made configuration (even if automatically generated) should be stored in 
`$XDG_CONFIG_HOME` and package-made configuration should be stored in `$XDG_DATA_DIRS`.

`theme-manager` will also use directories at `$XDG_STATE_HOME` and `$XDG_DATA_HOME`
to store the current state of the application and the generated presets respectively.
If the variables are not defined, `theme-manager` will use `$HOME/.local/state` and
`$HOME/.local/share` as defaults. You don't need to worry about these directories,
as they are for internal use of `theme-manager`.

:ref:`This example <example_root_directory_file_tree>` should help you understand 
how the root file tree shoud look like. 

When `theme-manager` finds a directory it's searching, it looks for:

theme-manager.toml
    The configuration file for `theme-manager`.

    .. warning:: 
        It doesn't have a use for now, might be removed.

applications/
    The directory that contains the application-specific configuration.
    It should contain only `TOML` or `JSON` files. **Remember to include the
    .toml or .json extension**, as `theme-manager` won't recognise the files
    without them.
    
    See the :ref:`application configuration <configuration_applications_start>`
    section for more details and how to write these configurations.

themes/
    The directory that contains the themes and their configuration. 
    It should have the themes' directories, each with their own `theme.toml` 
    or `theme.json` file. **Remember to include the .toml or .json extension**, 
    as `theme-manager` won't recognise the files without them. 
    
    See the :ref:`theme configuration <configuration_themes_start>` section
    for more details and how to write these configurations.

scripts/
    The directory that contains the scripts used in the configuration files. It should
    have three directories: `enabling_procedures`, `check_procedures` and `references`.
    All of them should contain only `.py` files.

    See the :ref:`scripts <configuration_scripts_start>` section for more details and
    how to write these scripts.

:ref:`This example <example_theme_manager_file_tree>` should help you understand how the `theme-manager`
file tree shoud look like.

.. note:: 
    The `TOML` and `JSON` documents should be written as defined by the `TOML Specification`_ [#f2]_ and the 
    `ECMA-404 Standard`_ [#f3]_ respectively. 

.. rubric:: Footnotes
.. [#f1] See the `XDG Base Directory Specification`_ 
    (`https://specifications.freedesktop.org/basedir-spec/latest/index.html <XDG Base Directory Specification>`_) 
    for more info about these variables and their default values.
.. [#f2] `TOML Specification`:  `https://toml.io/en/v1.0.0 <TOML Specification>`_
.. [#f3] `ECMA-404 Standard`: `https://ecma-international.org/publications-and-standards/standards/ecma-404/ <ECMA-404 Standard>`_

.. _TOML Specification: https://toml.io/en/v1.0.0
.. _ECMA-404 Standard: https://ecma-international.org/publications-and-standards/standards/ecma-404/
.. _XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/index.html