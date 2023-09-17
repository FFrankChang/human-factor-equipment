.. Lumache documentation master file, created by
   sphinx-quickstart on Wed Jul  5 14:39:59 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the TMSi Python Interface documentation!
=======================================================

.. note::

   This project is under active development.

This documentation describes the TMSi Python Interface (*TMSiPy*), what it does, how it should work and what you can and cannot expect from TMSi regarding 
this interface. Please read it through carefully. The TMSi Python Interface is a library for Python written by TMSi to interface the SAGA and APEX Device 
Drivers to Python.

.. warning:: 
   This documentation is written for the TMSi Python Interface V5.0.0.0 and higher. Please note that there have been **major changes** from V4.1.0.0 to V5.0.0.0 and higher.
   Please find the most important changes :ref:`here <changes-page-label>` to understand how to migrate your code from V4.1.0.0 to V5.0.0.0 and higher.


.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Getting started
     - Tutorials
     - Support
   * - New to the TMSi Python Interface or interested to learn more? Please take a look at the :ref:`Getting Started page <getting-started-page-label>` to learn how to :ref:`install <installation-page-label>` the TMSi Python Interface, what is :ref:`included <features-page-label>` and what :ref:`examples <examples-page-label>` you can follow to get acquainted with the Interface. 
     - Several tutorials have been included in the documentation to learn how to use the TMSi Python Interface. Get started with learning about the :ref:`Plotters <TMSi Plotter tutorial>`, about performing :ref:`EEG measurements <tutorial-eeg-page-label>` with APEX or :ref:`HD-EMG measurements <tutorial-emg-page-label>` with SAGA.
     - Do you have any questions about using the TMSi Python Interface? We cannot help you write your code, but any questions about using the TMSi Python Interface can be asked to your `local distributor <https://www.tmsi.com/distributors/?continent=18>`_.


.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Licensing
     - Documentation Contents
     - Indices
   * - The TMSi Python Interface is **free of charge** and distributed under the `Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_. The complete text of the license is included in LICENSE.txt, which can be found in the root folder of the TMSi Python Interface. TMSi has tested the interface, but cannot guarantee that it works under every circumstance, let alone that it will function in the experimental setup that you have in mind.
     - 
        .. toctree::
         :titlesonly:
         :maxdepth: 1

         getting_started/index_gs
         tutorials/tutorials
         changes
         code/modules
         release_notes
     - 
       * :ref:`genindex`
       * :ref:`modindex`
       * :ref:`search`

