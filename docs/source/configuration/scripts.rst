.. _configuration_scripts_start:

Scripts
=======

..
    application/enable/function/script
    check/script
    references/script

.. warning:: 
    When using a script that you didn't write yourself, be sure that the its code is safe. To execute scripts,
    `theme-manager` needs to import them as modules, so **everything at the global scope of the code will be
    executed, as well as the main function!** If you are not familiar with how imports work in Python, see
    the official Python documentation on `the import system`_ [#f1]_. 

When the available functions for enabling procedures, the types of check procedures or the default references
doesn't satisfy your needs, you can write them yourself **using Python**. This is the purpose of the support for scripts, 
mainly in the early stages of `theme-manager`. This section will teach you on how to write a script for `theme-manager`.
Be aware that, depending on where the script is called, `theme-manager` might pass different arguments to the
script and/or expect a specific variable type to be returned.

`theme-manager` will know the type of script based on it's directory. Inside the `scripts` folder, there should be one directory
for enabling procedures called `enabling_procedures`, one for check procedures called `check_procedures`, and one for references
called `references`. Inside them is where the `.py` files should be stored.

.. note:: 
    If you think your script should be part of the built-in procedures or the default references, please open an
    issue at the `GitHub repository`_ [#f2]_ describing what your script does or fork the repository, make the changes
    you want and open a pull request.

.. note:: 
    An example of what's described in this section can be found :ref:`here <example_script>`.

Every script should define one thing at the global scope of the code: a function called `main`.

`main`: ``function``
    This function is what `theme-manager` will call to do whatever is needed. 

    All `main` functions should expect the keyword argument `logger`. Aditional arguments and expected return value types
    are dependant on the script's purpose.

    `logger`: ``object``
        An object made to print information to `stdout` or `stderr` depending on the program's verbosity level. This object contains
        four methods that should be used instead of the builtin `print`, each one with their specific use cases: `debug`, `info`, `warn`
        and `error`. From the four, only `error` bypasses the `\-\-quiet` option. All of them require the argument `message`.

        `message`: ``string``
            The message that should be printed.

        `debug`: ``function``
            Used to print information that will be useful to solve any problems a user might have using the script. The messages sent
            using this method will only be printed if the `\-\-verbose` option is used twice. Requires the additional argument `module`.

            `module`: ``string``
                The name of the script. It's recommended to use the `__name__` variable.

            The messages sent using this method will be printed following the structure::

                [DEBUG:{module}] {message}

        `info`: ``function``
            Used to print information that allows the user to keep track of what the script is doing. The messages sent using this method will
            only be printed if the `\-\-verbose` option is used, at least, once. 

            The messages sent using this method will be printed following the structure::

                [INFO] {message}

        `warn`: ``function``
            Used to print warnings to `stderr` about things that aren't normal and might be unintentional or wrong, but don't prevent the 
            program from doing what it needs to do.

            The messages sent using this method will be printed following the structure::

                [WARNING] {message}

        `error`: ``function``
            Used to print errors to `stderr` and stop `theme-manager`'s execution. Requires the additional arguments `exit_code` and `module`.

            `exit_code`: ``integer``
                The exit code `theme-manager` should use.
            
            `module`: ``string``
                The name of the script. It's recommended to use the `__name__` variable.

            .. highlight:: none
            
            The messages sent using this method will be printed following the structure::
            
                [ERROR:{module}] {message}
                [ERROR] Ending theme-manager's execution.
            
            **USE THIS METHOD ONLY WHEN EXTREMELY NECESSARY**. Instead, try to handle the problem and use the `warn` method.

    If the script is an enabling procedure, `main` should expect additional positional arguments and keyword arguments using ``*args`` and ``**kwargs``, 
    its return value will be ignored and `theme-manager` will proceed with it's operation after the function's execution assuming the theme is already 
    enabled for the application that uses this script.
    
    If the script is a check procedure, `main` should expect additional positional arguments and keyword arguments using ``*args`` and ``**kwargs`` and
    `theme-manager` expects a boolean return value. If `main` returns `True`, the check succeeds, but if it returns `False`, the check fails.

    If the script is a reference, `main` should expect additional positional arguments and keywork arguments using ``*args`` and ``**kwargs``. 
    The reference that calls the script will be replaced with it's return value.

    .. `ref_type`: ``type``
    ..     The type of the reference. Its possible values are listed at the :ref:`references section <configuration_references_start>`.

.. rubric:: Footnotes
.. [#f1] Python's documentation of `the import system`_: `https://docs.python.org/3/reference/import.html <the import system>`_
.. [#f2] `GitHub repository`_: `https://github.com/Limones-07/theme-manager <GitHub repository>`_

.. _the import system: https://docs.python.org/3/reference/import.html
.. _GitHub repository: https://github.com/Limones-07/theme-manager