.. _configuration_files_start:

Where to place directories and files
====================================

`theme-manager` looks for same named directories on the folders specified by the 
environment variables `$XDG_DATA_HOME` and `$XDG_DATA_DIRS` as defined by
the `XDG Base Directory Specification`_ [#f1]_. If they are not defined, `theme-manager` 
will look for its directories on `$HOME/.local/share`, `/usr/local/share` and `/usr/share`, 
in this order. :ref:`This example <examples_root_directory_file_tree>` should help you understand 
how the root file tree shoud look like.

When `theme-manager` finds a directory it's searching, it looks for:

theme-manager.toml
    The configuration file for `theme-manager`.

    .. warning:: 
        It doesn't have a use for now, might be removed.

themes/
    The directory that contains the themes and their configuration. 
    Should contain a `themes.toml` file and the themes' directories, 
    each with their own `theme.toml` file. The themes may have a `theme.json`
    configuration file instead, but never both. 
    
    See the :ref:`theme configuration <configuration_themes_start>` section
    for more details and how to write these configurations.

applications/
    The directory that contains the application-specific configuration.
    Should contain just `TOML` or `JSON` files. 
    
    See the :ref:`application configuration <configuration_applications_start>`
    section for more details and how to write these configurations.

:ref:`This example <examples_theme_manager_file_tree>` should help you understand how the `theme-manager`
file tree shoud look like.

.. note:: 
    The `TOML` and `JSON` documents should be written as defined by the `TOML Specification`_ [#f2]_ and the 
    `ECMA-404 Standard`_ [#f3]_, in this order. 

.. note:: 
    The theme and application configuration can be done by a package. 

.. rubric:: Footnotes
.. [#f1] See the `XDG Base Directory Specification`_ 
    (`https://specifications.freedesktop.org/basedir-spec/latest/index.html <XDG Base Directory Specification>`_) 
    for more info about these variables and their default values.
.. [#f2] `TOML Specification`:  `https://toml.io/en/v1.0.0 <TOML Specification>`_
.. [#f3] `ECMA-404 Standard`: `https://ecma-international.org/publications-and-standards/standards/ecma-404/ <ECMA-404 Standard>`_

.. _TOML Specification: https://toml.io/en/v1.0.0
.. _ECMA-404 Standard: https://ecma-international.org/publications-and-standards/standards/ecma-404/
.. _XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/index.html