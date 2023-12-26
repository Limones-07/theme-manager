.. _configuration_themes_start:

Configuring themes
==================

To configure a theme, you need a `TOML` or a `JSON` file. The recommended way for manually configuration
is to write a `TOML` file just because it's easier, but there is no other difference between the two aside
from the syntax. Leave the `JSON` files for automatically generated configurations.

Using TOML files
----------------

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