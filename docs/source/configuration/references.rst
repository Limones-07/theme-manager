.. _configuration_references_start:

References
==========

References are the variables `theme-manager` understands. For every string that 
`theme-manager` needs to interpret, first it verifies the existance of references, 
which are prefixed by an at sign (`@`). Then, `theme-manager` replaces the reference 
with the value it represents. So, for example, if the string `"@H/.config/theme-manager"`
is given in any configuration entry, `theme-manager` will expand it to
`/home/user/.config/theme-manager`. This will happen in **any** string **except for
strings that define the id/name of something, for example, an enabling procedure, an application
or a theme.**. 

.. note:: 
    When a string is passed containing **only** a reference, `theme-manager` will change
    the type of the value to whatever the type of the reference is. So, for example, if
    the string `"@foo"` is passed to an entry and the type of the `@foo` reference is derived
    from `integer`, the value passed won't be interpreted as a `string`, but as an `integer` 
    instead.

References can be created on the configuration of `enabling procedures`. When you create
a `requires` table/object, you are defining an reference with the name determined by the
`id` entry and the type determined by the `type` entry. Later, they can be used, for example, 
as arguments for a shell command, but only in the same procedure. References defined on a
procedure `foo` cannot be used on a procedure `bar`, neither on a `baz`. References defined on a
`requires` table/object are only available to the same procedure's scope.

Be aware that **user-defined references are always on lowercase**. Even if the `id` entry on
an enabling procedure if all on uppercase, it will be converted to lowercase before being usable.
In contrast, all of the default references are on uppercase.

.. note:: 
    If you want to see an example, references are used both on the 
    :ref:`application <example_application_configuration>` and the 
    :ref:`theme <example_theme_configuration>` configuration examples.

Reference types
---------------

When defining a reference on the enabling procedures, you need to specify a type. Depending on the
type, `theme-manager` will or will not validate it when it's used. For example, when an enabling 
procedure requires a path, `theme-manager` will check if the value passed to it on a theme's configuration
is actually a path. If not, `theme-manager`'s operation is aborted. 

Some types are derived from others. When that happens, `theme-manager` will validate the value of the reference
as if it was of every parent type. For example, a `path` reference will be validated as both a `path` and a `string`.

These are the currently existing reference types:

`string`:
    One of the basic types. To be valid, it needs to follow the `TOML` or `JSON` syntax for strings. On scripts,
    `ref_type` will be ``string``.

`path`:
    Type derived from `string`. To be valid, it must be able to create a `pathlib.Path <pathlib>`_ object [#f1]_ and must be absolute.
    On scripts, `ref_type` will be ``string``.

`number`:
    One of the basic types. To be valid, it needs to follow the `TOML` syntax for integers or floats
    or the `JSON` syntax for numbers. On scripts, `ref_type` will be ``float``.

`integer`:
    Type derived from `number`. To be valid, it **must not** be a `TOML` float or a `JSON` number 
    **with a decimal point or an exponent**. On scripts, `ref_type` will be ``int``.

`float`:
    One of the basic types. To be valid, it **must not** be a `TOML` integer or a `JSON` number
    **without a decimal point or an exponent**. On scripts, `ref_type` will be ``float``.

`boolean`:
    One of the basic types. To be valid, it needs to follow the `TOML` or `JSON` syntax for booleans.
    On scripts, `ref_type` will be ``bool``.

..
    `null`: 
        One of the basic types. To be valid, it needs to follow the `JSON` syntax for `null` values. 
        As `null` doesn't exists in `TOML`, `false` can be used instead. On scripts, `ref_type` will be ``bool``.
        Why is this here??? What's the purpose of a null reference?????

Default references
------------------

These are the default references:

`@THEME_DIR`:
    Refers to the theme's directory, the same of the `theme.toml` or `theme.json` file.

`@HOME`:
    Refers to the user's home directory. 

`@SCRIPT:{script_name}`:
    This is a special reference. To know to value it needs to be replaced with, `theme-manager`
    will execute the script between curly braces and replace the reference with the returned
    value. See the :ref:`scripts <configuration_scripts_start>` section to know how to write
    a script.

.. rubric:: Footnotes
.. [#f1] See the Python `pathlib`_ documentation for more details: (`https://docs.python.org/3/library/pathlib.html <pathlib>`_)

.. _pathlib: https://docs.python.org/3/library/pathlib.html