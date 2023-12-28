.. _configuration_applications_start:

Configuring applications
========================

To configure an application, you need a `TOML` or a `JSON` file. The recommended file type to configure manually
is `TOML` because of its simplicity, but there is no difference between the two aside from the syntax.
Leave the `JSON` files for automatically generated configuration (unless you want to use `JSON`, it doesn't really matter).

.. note:: 
    An example of what's described in this section can be found 
    :ref:`here <example_application_configuration>`.

Using `TOML` files
------------------

You need to define three things on the root of the document: the table `id`, the array of tables `check_procedures`
and the array of tables `enabling_procedures`.

`id`: ``table``
    Defines how the application will be identified. It requires two entries: `desktop_entry` and `name`. 

    `desktop_entry`: ``string`` || ``false``
        Specifies the `.desktop` file corresponding to the application. It will be used to determine the name of the
        application based on the desktop file using the `Name` entry as defined by the 
        `XDG Desktop Entry Specification`_ [#f1]_. If `theme-manager` cannot parse the name from the file or the string
        passed is not a valid path, it will use the `name` entry instead. If you want to use the `name` entry instead of 
        the desktop entry on purpouse, pass ``false`` to this entry.

    `name`: ``string``
        Specifies the fallback name used by `theme-manager` to identify this application if it can't use the desktop entry.

`check_procedures`: ``array of tables``
    Specifies how `theme-manager` should verify the installation of the application. Each table inside the array
    defines one check procedure, and must be composed of, at least, the entry `type`. Depending on its value,
    more entries are required.

    `type`: ``string``
        Determines which check procedure `theme-manager` will execute to verify the installation of the application. 
        See the :ref:`check procedures <configuration_check_procedures_start>` section to know the possible values.

`enabling_procedures`: ``array of tables``
    Specifies how `theme-manager` can enable a theme for the application. Each table inside the array defines one
    procedure the theme can use to enable itself, and must be composed of three major entries: the string `id`, 
    the array of tables `requires` and the table `function`.

    `id`: ``string``
        Defines how the procedure will be identified by the themes. 
    
    `requires`: ``array of tables``
        Defines the arguments of this procedure. These arguments can be used on the `function` table as a
        reference. Each table inside the array defines one argument and must be composed of two entries:
        the strings `id` and `type`.

        `id`: ``string``
            Defines the name of the argument. It's also the name of the reference.

        `type`: ``string``
            Defines the type of the reference.

    `function`: ``table``
        Defines what `theme-manager` needs to do to enable a theme for the application. Must be composed of,
        at least, the entry `type`. Depending on its value, more entries are required.

        `type`: ``string``
            Defines what is the operation `theme-manager` needs to do to enable the requested theme.
            Possible values are:

            `create_symlink`:
                Creates a symbolic link. Requires two additional entries: the strings `target` and `directory`.
                
                `target`: ``string``
                    Specifies where the link should point to. 

                `directory`: ``string``
                    Specifies where the link should be created. If the given path is not to a directory and is to a file instead,
                    creates the link as the file specified.

            `shell`:
                Runs a shell command. It requires two additional entries: the string `command`
                and the array `args`.

                `command`: ``string``
                    Defines what command will be executed in the shell.

                `args`: ``array``
                    Defines what are the arguments for the command. Each element will be concatenated with the previous
                    using a space character (`U+0020`), being the first argument concatenated with the command string.
                    If you don't need any arguments, leave the array empty.

            `script`:
                Used when none of the existing functions meet your requirements. It allows you to write a Python script
                and use it as a function. See the section for :ref:`scripts <configuration_scripts_start>` too learn what
                you need to use one. Requires one additional entry: `name`.

                `name`: ``string``
                    The name of the script without the `.py` extension. 

Using `JSON` files
------------------

You need to define three things on the root of the document: the object `id` and the arrays `check_procedures`
and `enabling_procedures`.

`id`: ``object``
    Defines how the application will be identified. It requires two entries: `desktop_entry` and `name`. 

    `desktop_entry`: ``string`` || ``null``
        Specifies the `.desktop` file corresponding to the application. It will be used to determine the name of the
        application based on the desktop file using the `Name` entry as defined by the 
        `XDG Desktop Entry Specification`_ [#f1]_. If `theme-manager` cannot parse the name from the file or the string
        passed is not a valid path, it will use the `name` entry instead. If you want to use the `name` entry instead of
        the desktop entry on purpouse, pass ``null`` to this entry.

    `name`: ``string``
        Specifies the fallback name used by `theme-manager` to identify this application if it can't use the desktop entry.

`check_procedures`: ``array of objects``
    Specifies how `theme-manager` should verify the installation of the application. Each object inside the array
    defines one check procedure, and must be composed of, at least, the entry `type`. Depending on its value,
    more entries are required.

    `type`: ``string``
        Determines which check procedure `theme-manager` will execute to verify the installation of the application. 
        See the :ref:`check procedures <configuration_check_procedures_start>` section to know the possible values.

`enabling_procedures`: ``array of objects``
    Specifies how `theme-manager` can enable a theme for the application. Each object inside the array defines one
    procedure the theme can use to enable itself, and must be composed of three major entries: the string `id`, 
    the array of objects `requires` and the object `function`.

    `id`: ``string``
        Defines how the procedure will be identified by the themes.
    
    `requires`: ``array of objects``
        Defines the arguments of this procedure. These arguments can be used on the `function` object as a
        reference. Each object inside the array defines one argument and must be composed of two entries:
        the strings `id` and `type`.

        `id`: ``string``
            Defines the name of the argument. It's also the name of the reference.

        `type`: ``string``
            Defines the type of the reference.

    `function`: ``object``
        Defines what `theme-manager` needs to do to enable a theme for the application. Must be composed of,
        at least, the entry `type`. Depending on its value, more entries are required.

        `type`: ``string``
            Defines what is the operation `theme-manager` needs to do to enable the requested theme.
            Possible values are:

            `create_symlink`:
                Creates a symbolic link. Requires two additional entries: the strings `target` and `directory`.
                
                `target`: ``string``
                    Specifies where the link should point to. 

                `directory`: ``string``
                    Specifies where the link should be created. If the given path is not to a directory and is to a file instead,
                    creates the link as the file specified.

            `shell`:
                Runs a shell command. It requires two additional entries: the string `command`
                and the array `args`.

                `command`: ``string``
                    Defines what command will be executed in the shell.

                `args`: ``array``
                    Defines what are the arguments for the command. Each element will be concatenated with the previous
                    using a space character (`U+0020`), being the first argument concatenated with the command string.
                    If you don't need any arguments, leave the array empty.

            `script`:
                Used when none of the existing functions meet your requirements. It allows you to write a Python script
                and use it as a function. See the section for :ref:`scripts <configuration_scripts_start>` too learn what
                you need to use one. Requires one additional entry: `name`.

                `name`: ``string``
                    The name of the script without the `.py` extension. 

.. rubric:: Footnotes
.. [#f1] See the `XDG Desktop Entry Specification`_ for more info: 
    (`https://specifications.freedesktop.org/desktop-entry-spec/latest/index.html <XDG Desktop Entry Specification>`_).

.. _`XDG Desktop Entry Specification`: https://specifications.freedesktop.org/desktop-entry-spec/latest/index.html