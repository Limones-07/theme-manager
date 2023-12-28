.. _configuration_check_procedures_start:

Check procedures
================

:ref:`As explained earlier <configuration_configuration_check_procedures>`, 
both applications and themes should have their installations checked. This section will talk about each one of the
existing procedures and how to use them. 

.. note:: 
    Unless explicitly said, there is no value type difference between the `TOML` and `JSON` files. 

`json_entry`:
    Looks for a specific entry in a `JSON` file and compares it's value with another pre-configured value. 
    If they are equal, the check procedure succeeds. Requires three additional arguments: `file`, `entry`
    and `value`.

    `file`: ``string``
        Determines which file contains the searched entry.

    `entry`: ``array``
        Determines what is the entry that contains the value that will be compared. Each element of the array
        is one piece of the path to the desired value. For example, to reach ``parent.subparent.id``, the array
        should be ``["parent", "identifier", "id"]``. If one of the elements have a dot (`.`) in it, it will not
        be divided. 

        If one of the elements is a question mark (`?`), it means that the value can be in any element of
        an **array** in the `JSON` file, so `theme-manager` will iterate through every value in the array and continue
        searching until it finds the desired entry. If the configured entry is found in one of the iterations but
        the value doesn't march the desired one, `theme-manager` will continue searching. The check procedure will
        only fail if the value can't be found in any of the iterations. However, if it is found in any iteration,
        the check procedure will succeed.
    
    `value`: ``number`` || ``string`` || ``true`` || ``false`` || ``null``
        Determines what the entry value should be.

`command_exists`:
    Looks for a command on the directories specified by the `$PATH` environment variable, similarly to the
    `which` shell command. If it exists, the check procedure succeeds. Requires one additional entry: `command`.

    `command`: ``string``
        Determines which command should be searched for.

`file_exists`:
    Checks if a file exists. If it does, the check procedure succeeds. Requires one additional entry: `file`.
    Depending on the value of `file`, the additional entries `path` and `recursive` will be required.

    `file`: ``string``
        Determines the path of the target file. If it's not an absolute path, the `path` and `recursive` 
        entries are required.

    `path`: ``string``
        Determines where `theme-manager` should look for the target file. More than one path can be specified 
        by separating them with a colon (`:`), like on the `$PATH` environment variable.
    
    `recursive`: ``boolean``
        Specifies if the given paths should be searched recursively.

`directory_exists`:
    Checks if a directory exists. If it does, the check procedure succeeds. Requires one additional entry: `directory`.
    Depending on the value of `directory`, the additional entries `path` and `recursive` will be required.

    `directory`: ``string``
        Determines the path of the target directory. If it's not an absolute path, the `path` and `recursive` 
        entries are required.
    
    `path`: ``string``
        Determines where `theme-manager` should look for the target directory. More than one path can be specified 
        by separating them with a colon (`:`), like on the `$PATH` environment variable.
    
    `recursive`: ``boolean``
        Specifies if the given paths should be searched recursively.

`script`:
    This is used when none of the existing procedures meet your requirements. It allows you to write a Python script
    and use it as a check procedure. See the section for :ref:`scripts <configuration_scripts_start>` too learn what
    you need to use one. Requires one additional entry: `name`.

    `name`: ``string``
        The name of the script without the `.py` extension. 