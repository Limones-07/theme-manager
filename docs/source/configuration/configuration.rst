.. _configuration_start:

Configuration
=============

For `theme-manager` to work properly, it needs to be able to verify if its themes are properly installed
and enable them. To acomplish that, it uses each themes' configuration files to specify how these two things 
should be done. It also needs to know how to modify some application-specific configuration files to apply 
things like font styles and color schemes. 

There are two major categories of `theme-manager` configuration files: applications configuration files and
themes configuration files. 

The first is used to tell `theme-manager` what to do when trying to modify a setting from a specific application. 
For example, it specifies what is the file and `JSON` entry `theme-manager` needs to modify to mofidy the theme of 
VS Code. These instructions are called `enabling procedures`.

The second is used to specify which applications a theme supports and which procedure needs to be executed to enable
itself.

Be aware that inside the configuration documents, environment variables and the tilde (~) symbol are not interpreted 
by `theme-manager` (they might be interpreted if the string goes through a shell at some point, but it isn't guaranteed
to happen). To provide access to some special values like the current directory or the home folder, `references` exist.
See the :ref:`references <configuration_references_start>` section to know what they are and how to use them.

The following sections will teach you where to put these files and how to write them.

.. toctree:: 
    :hidden:

    files
    applications
    themes
    references
    scripts