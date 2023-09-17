.. _installation-page-label:

Installing the interface
==============================
The installation requirements and installation method can be found here.

Installation requirements
--------------------------------
The TMSi Python Interface requires the following for Windows computers:

* A computer with Windows 10, 64 bit.
* Device driver:
   * APEX Device Driver 1.2.0.0 or higher.
   * SAGA Device Driver 2.0.0.0.
* Python version 3.9 or higher 
   * `Python for Windows <https://www.python.org/downloads/release/python-3912/>`_. Please ensure that the *path_length_limit* parameter is disabled during Python installation.

The library has been tested on the following Python versions:

* Python 3.9.12 (Windows 10 / 64 bit)
* Python 3.10.5 (Windows 10 / 64 bit)

Other Python versions have not been tested with this release (V5.1.0.0)

Installation
----------------------
.. note:: 

    Please make sure the TMSi Device Driver has been succesfully installed before using the TMSi Python Interface

The installers can be used to install additional Python libraries using virtual environments. In order to run this script, you need to ensure that Python is available 
on the system’s path, which can be confirmed during Python installation or manually via Windows’ Environment Variables. To use the installers simply double click on 
the installer corresponding to your Python version. A window will open showing feedback regarding the installation process. Wait for the installation to finish 
completely and press any key to exit. The installation process can take a couple of minutes.

Using Spyder IDE
^^^^^^^^^^^^^^^^^^^^^^^^^^^
When the Spyder IDE is used, please use v5.2.2 (as the virtual environment uses the libraries used by this Spyder version). Alternatively, you could upgrade the spyder-kernels library to the version mentioned by Spyder.
In Spyder, the Python interpreter needs to be changed to the virtual environment’s Python installation that has been created. The custom environment can be configured in *Preferences → Python interpreter*. The specific file to select can be found in the 
following path: *.../tmsi_python_interface/.venv/Scripts/python.exe*. 

Secondly, Spyder's working directory needs to be changed, so that all libraries can be used correctly. This can be done as follows: *Tools → Preferences →
Run → Working directory settings → The following directory: → C:/Users/../../tmsi-python-interface-V5.1.0.0*. If preferred, Spyder's default startup directory can be edited as well:
*Tools → Preferences → Current working directory → ... → The following directory: → C:/Users/../../tmsi-python-interface-V5.1.0.0*. The path that is filled out, should match the path where
the TMSi Python interface has been saved.

A final step in using Spyder is to configure the IPython Graphics Backed to ‘inline’. This can be configured from Spyder’s menu bar as follows: *Tools → Preferences →
IPython Console → Graphics → Graphics backend → Inline*. Plots can be made interactive again, for instance for analysis purposes, using the IPython library that 
comes with Spyder. This can be done using the two lines of code below:

.. code-block:: python

    ipython = get_ipython()
    ipython.magic("matplotlib qt")

