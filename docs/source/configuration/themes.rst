.. _configuration_themes_start:

Configuring themes
==================

To configure a theme, you need a `TOML` or a `JSON` file. The recommended file type to configure manually
is `TOML` because of its simplicity, but there is no other difference between the two aside from the syntax.
Leave the `JSON` files for automatically generated configuration.

Using `TOML` files
------------------

.. note:: 
    An example of what's described in this subsection can be found 
    :ref:`here <examples_theme_configuration_theme_toml>`.

You need to define three things on the root of the document: the string `name`, the array of
tables `installation_check` and the array of tables `applications`.

`name` (``string``):
    Defines the name of the theme. It will be used to identify this theme wherever is required. 

    .. note:: 
        This entry is case-sensitive. When you need to mention a theme, pay attention to this.
    
`installation_check` (``array of tables``):
    .. note:: 
        This is different from the `installation_check` from the application configuration files.

    Specifies how `theme-manager` should verify the installation of the theme. 
    Each table inside the array defines one check procedure, and should be composed of, at least, 
    two entries: `required_by` and `type`. Depending on the `type` value, more values are required.

    `required_by` (``string``):
        Specifies which application needs this check to succeed. If it isn't the application involved
        with the running `theme-manager` operation, the check will be skipped.

    `type` (``string``):
        Determines what `theme-manager` will do to verify the installation of the theme. Currently,
        the supported options are: ...