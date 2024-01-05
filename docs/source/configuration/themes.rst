.. _configuration_themes_start:

Configuring themes
==================

To configure a theme, you need a `TOML` or a `JSON` file. The recommended file type to configure manually
is `TOML` because of its simplicity, but there is no difference between the two aside from the syntax.
Leave the `JSON` files for automatically generated configuration (unless you want to use `JSON`, it doesn't really matter).

.. note:: 
    An example of what's described in this section can be found 
    :ref:`here <example_theme_configuration>`.

Using `TOML` files
------------------

You need to define three things on the root of the document: the string `name`, the array of
tables `check_procedures` and the array of tables `applications`.

`name`: ``string``
    Defines the name of the theme. It will be used to identify this theme wherever is required. 

    .. note:: 
        This entry is case-sensitive. When you need to mention a theme, pay attention to this.
    
`check_procedures`: ``array of tables``
    Specifies how `theme-manager` should verify the installation of the theme. Each table inside the 
    array defines one check procedure, and must be composed of, at least, two entries: 
    `required_by` and `type`. Depending on the `type` value, more entries are required.

    `required_by`: ``string``
        Specifies which application needs this check to succeed. If it isn't the application involved
        with the running `theme-manager` operation or the passed string is empty, the check will be skipped.

    `type`: ``string``
        Determines which check procedure `theme-manager` will execute to verify the installation of the application. 
        See the :ref:`check procedures <configuration_check_procedures_start>` section to know the possible values.

`applications`: ``array of tables``
    Specifies how `theme-manager` should enable the theme on each application. Each table inside the array
    defines one application, and must be composed of, at least, two entries: `id` and `procedure`.

    `id`: ``string``
        Specifies the name of the application this table is configuring. It must match the name of a configured
        application, being the name parsed from the desktop file or explicitly defined on the `name` entry.
    
    `procedure`: ``table``
        Specifies what `theme-manager` should do to enable this theme. Requires, at least, the string `id`.
        Depending on its value, more arguments will be required.

        `id`: ``string``
            Specifies which enabling procedure of the application should be used. This value must be the same of
            the desired procedure's `id` entry. If the specified procedure requires any arguments, they must be
            passed as additional entries.

Using `JSON` files
------------------

You need to define three things on the root of the document: the string `name`, the array of
objects `check_procedures` and the array of objects `applications`.

`name`: ``string``
    Defines the name of the theme. It will be used to identify this theme wherever is required. 

    .. note:: 
        This entry is case-sensitive. When you need to mention a theme, pay attention to this.
    
`check_procedures`: ``array of objects``
    Specifies how `theme-manager` should verify the installation of the object. Each object inside 
    the array defines one check procedure, and must be composed of, at least, two entries: 
    `required_by` and `type`. Depending on the `type` value, more entries are required.

    `required_by`: ``string``
        Specifies which application needs this check to succeed. If it isn't the application involved
        with the running `theme-manager` operation or the passed string is empty, the check will be skipped.

    `type`: ``string``
        Determines which check procedure `theme-manager` will execute to verify the installation of the application. 
        See the :ref:`check procedures <configuration_check_procedures_start>` section to know the possible values.

`applications`: ``array of objects``
    Specifies how `theme-manager` should enable the theme on each application. Each object inside the array
    defines one application, and must be composed of, at least, two entries: `id` and `procedure`.

    `id`: ``string``
        Specifies the name of the application this table is configuring. It must match the name of a configured
        application, being the name parsed from the desktop file or explicitly defined on the `name` entry.
    
    `procedure`: ``object``
        Specifies what `theme-manager` should do to enable this theme. Requires, at least, the string `id`.
        Depending on its value, more arguments will be required.

        `id`: ``string``
            Specifies which enabling procedure of the application should be used. This value must be the same of
            the desired procedure's `id` entry. If the specified procedure requires any arguments, they must be
            passed as additional entries.
