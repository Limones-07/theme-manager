theme-manager
=============

"theme-manager" is a command-line tool for managing themes in your Linux installation based on each theme's configuration.

You can check the documentation online at http://theme-manager.readthedocs.io/.

**It's still in development stage. Please wait for the first release.**

NOTHING HERE WORKS. DON'T TRY TO RUN OR INSTALL ANYTHING HERE YET.
------------------------------------------------------------------

Installation
------------

You can install `theme-manager` from the package ``theme-manager-git`` using an AUR helper or manually.

With an AUR helper...::

    paru -S theme-manager-git

Manually...::

    git clone https://aur.archlinux.org/theme-manager-git.git
    cd theme-manager/
    makepkg -si

.. note:: 
    Do not install `theme-manager` using pip directly, as it will not install the manual page and
    the default configurations (unless you don't want/need both).