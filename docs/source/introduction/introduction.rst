.. _introduction_start:

Introduction
============

.. warning:: 
    THIS APPLICATION IS IN PRE-ALPHA. NOTHING HERE WORKS (yet).

About the documentation
-----------------------

This documentation will walk you through theme configuration, 
application configuration and usage of the tool. 

.. note:: 
    For installation and uninstallation instructions, read the `README.rst` file on the GitHub repository.

What does it do?
----------------

`theme-manager` simplifies the process of managing the style of your system, 
allowing you to manage every (configured) applications' theme and style 
using a single tool. It can apply a style globally as well as modify 
the style of a single application specifically.

.. note:: 
    It doesn't have a GUI (for now). However, you can create an application
    that uses `theme-manager` as a backend (eg. a widget using Eww [#f1]_).

How does it do that?
--------------------

This application uses configuration files to know where each theme's data is,
what that data specifies and how to apply them. The purpose of this program is
to allow the user to enable a theme in as many applications as possible using 
a single command. See the :ref:`theme <examples_theme_configuration>` and 
:ref:`application <examples_application_configuration>` configuration file
examples to know how they look like and the :ref:`configuration <configuration_start>`
section to know how `theme-manager` interprets them. 

Current features
----------------

* Nothing at all 🔥🔥🔥

.. _introduction_todo:

TODO
----

* Apply a theme.
* Configure each application individually.
* Create a configuration file interactively.
* Basically everything.

.. rubric:: Footnotes
.. [#f1] `Eww`_ (or ElKowars Wacky Widgets): `https://github.com/elkowar/eww <Eww>`_

.. _Eww: https://github.com/elkowar/eww