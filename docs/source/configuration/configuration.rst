.. _configuration_start:

Configuration
=============

For `theme-manager` to work properly, it needs to be able to verify if its themes are properly installed
and enable them. For that, it uses each themes' configuration files to specify how these two things should
be done. It also needs to know how to modify some application-specific configuration files to set up things
like font styles and color schemes. This section will show where to put these files and how to write them.

:ref:`TODO <introduction_todo>`: Create a way to configure themes and applications interactively. 

.. _configuration_where_to_place_directories_and_files:

Where to place directories and files
------------------------------------

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
    See the :ref:`theme configuration <configuration_configuring_themes>` section
    for more details.

applications/
    The directory that contains the application-specific configuration.
    Should contain just `TOML` or `JSON` files. 
    See the :ref:`application configuration <configuration_configuring_applications>`
    section for more detail.

:ref:`This example <examples_theme_manager_file_tree>` should help you understand how the `theme-manager`
file tree shoud look like.

.. note:: 
    The `TOML` and `JSON` documents should be written as defined by the `TOML Specification`_ [#f2]_ and the 
    `ECMA-404 Standard`_ [#f3]_, in this order. 

.. note:: 
    The theme and application configuration can be done by a package. 

.. _configuration_configuring_themes:

Configuring themes
------------------

To configure a theme, you need a `TOML` or a `JSON` file. The recommended way for manually configuration
is to write a `TOML` file just because it's easier, but there is no other difference between the two aside
from the syntax. Leave the `JSON` files for automatically generated configurations.

Using TOML files
^^^^^^^^^^^^^^^^

You need to define two things on the root of the document: the string ``name`` and the array of
tables ``applications``.

`name` entry:
    Here you define the name of the theme. It will be used to identify this theme.
    It can be composed by any alphanumeric characters and whitespaces. 
    .. It's recommended to only use ASCII characters, other Unicode characters may cause unintended behavior.

    .. note:: 
        This entry is case-sensitive. When you need to mention a theme, pay attention to this.

The ``applications`` array is where you specify how the theme is applied on each application. For that,
you create a table for every application inside the array. 

.. _configuration_configuring_applications:

Configuring applications
------------------------

be sus

.. rubric:: Footnotes
.. [#f1] See the `XDG Base Directory Specification`_ 
    (`https://specifications.freedesktop.org/basedir-spec/latest/index.html <XDG Base Directory Specification>`_) 
    for more info about these variables and their default values.
.. [#f2] `TOML Specification`:  `https://toml.io/en/v1.0.0 <TOML Specification>`_
.. [#f3] `ECMA-404 Standard`: `https://ecma-international.org/publications-and-standards/standards/ecma-404/ <ECMA-404 Standard>`_

.. _TOML Specification: https://toml.io/en/v1.0.0
.. _ECMA-404 Standard: https://ecma-international.org/publications-and-standards/standards/ecma-404/
.. _XDG Base Directory Specification: https://specifications.freedesktop.org/basedir-spec/latest/index.html