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
    This function is what `theme-manager` will call to do whatever is needed. Before calling this function, `theme-manager`
    overrides the `print` function with one from `theme-manager`'s logging utility, so it doesn't bypass the verbosity level.
    Everything that the script tries to print will be printed as a debug message. This function should also not depend on user
    input, as the `input` function might be overridden with `None` if the user requires no user interaction.

    All `main` functions should expect five keyword arguments: `theme-directory`, `user-home`, `xdg-config-home`, `xdg-data-dirs`
    and `Error`.
    Positional arguments and expected return value types are dependant on the script's purpose.

    `theme-directory`: ``string``
        The absolute path to the directory of the theme that needs to be enabled.
    
    `user-home`: ``string``
        The absolute path to the user's home folder.

    `xdg-config-home`: ``string``
        The absolute path to the XDG config home as defined by the `XDG Base Directory Specification`.
    
    `xdg-data-dirs`: ``string``
        The absolute paths to the XDG data directories separatad by colons (`:`) as defined by the `XDG Base Directory Specification`.

    `Error`: ``class``
        A class made to transmit information related to an error that might occur during the execution of the function. If something
        goes wrong in the script, `main` **must** return an object of this class instead of raising an exception. `Error`'s constructor 
        expects two arguments: the string `message` and the integer `exit_code`.

        `message`: ``string``
            The message to be printed as the error message.
        
        `exit_code`: ``int``
            The exit code `theme-manager` should use. It's highly recommended to follow what's specified at `/usr/include/sysexits.h`.
    
    If the script is an enabling procedure, no positional arguments are required, `main`'s return value will be ignored and `theme-manager` 
    will proceed with it's operation after the function's executioncassuming the theme is already enabled for the application that uses 
    this script.
    
    If the script is a check procedure, no positional arguments are required and `theme-manager` expects a boolean return value. 
    If `main` returns `True`, the check succeeds, but if it returns `False`, the check fails. 

    If the script is a reference, the positional argument `ref_type` is required and `theme-manager` expects a `ref_type` return value.
    After `theme-manager` verifies if the returned value if actually from the expected type, the reference will be replaced with whatever 
    is the return value.

    `ref_type`: ``type``
        The type of the reference. Its possible values are listed at the :ref:`references section <configuration_references_start>`.


.. rubric:: Footnotes
.. [#f1] Python's documentation of `the import system`_: `https://docs.python.org/3/reference/import.html <the import system>`_
.. [#f2] `GitHub repository`_: `https://github.com/Limones-07/theme-manager <GitHub repository>`_

.. _the import system: https://docs.python.org/3/reference/import.html
.. _GitHub repository: https://github.com/Limones-07/theme-manager