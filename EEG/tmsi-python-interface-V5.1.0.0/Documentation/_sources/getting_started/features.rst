.. _features-page-label:

Features
=================
The code in the TMSi Python Interface provides a Python library that can be used to control TMSi SAGA and/or APEX devices. The goal of this library is to provide an easy and intuitive way 
of accessing TMSi devices using Python. You can configure your experiments, write your own code or turn to supported libraries.

Functionality
------------------------

The library provides the following functionality:

* Device control:

  * SAGA: Sampling over USB for the Docking Station, and sampling over electrical (docked), optical and wireless interface for the Data Recorder.
  * APEX: Sampling over USB or Bluetooth.

* (Limited) live plotting of sampled data.
* (Limited) live filtering of sampled data.
* Sampling in impedance mode and (limited) live plotting of impedance values pre-measurement. Live impedance acquisition during data acquisition is possible with APEX.
* Changing the device configuration, including saving and loading the configuration using an XML-structured format.
* Directly saving sampled data to Poly5 file format or XDF file format.
* Offline conversion of sampled data from Poly5 file format to EDF file format.
* Loading data from Poly5, XDF or EDF file format and plotting data for viewing purposes.
* Catching device related errors. However, no typical error handling has been included.
* Writing to a LabStreamingLayer (LSL) stream outlet.
* Offline synchronization of files recorded with LSL.
* (Limited) live plotting of the sampled data in a heatmap, specifically designed for HD-EMG applications. Textile HD-EMG grids’ configuration is included (not applicable to APEX).
* Downloading recordings stored on SAGA’s and APEX' onboard memory.

* Configuring the device for a card recording:

  * SAGA: backup logging or button start.
  * APEX: button start or timed recording.
  
* Possibility to send triggers from Python to SAGA or APEX via the USB-TTL module.

The library does not (yet) support the following features:

* SAGA: Configuring the card to start a scheduled recording.

Lab Streaming Layer Intergration
--------------------------------------
LabStreamingLayer (LSL) is a separate program/library used to stream and record data. In order to use the TMSi Python Interface in combination with LSL, the liblsl-library has to be installed 
separately. More information on LSL, including ‘getting started’ information, can be found in the `documentation <https://labstreaminglayer.readthedocs.io/info/intro.html>`_ of LabStreamingLayer itself.
When using the TMSi Python Interface in combination with LSL, the following warning can show up: ‘Couldn't create multicast responder for 224.0.0.1 (set_option: A socket operation was attempted to an unreachable host)’. 
This warning originates form the liblsl-library and can't be solved by TMSi unfortunately. The warning does not influence the connection between the 
TMSi Python interface and LSL and can simply be ignored. Please find information on how to use LSL `here <https://knowledge.tmsi.com/how-can-i-synchronise-two-saga-amplifiers>`_.

Synchronization
^^^^^^^^^^^^^^^^^^^^^^^^^
Files recorded using the LSL-based LabRecorder applications contain separate streams for each device that made data available to the LSL platform. TMSi 
has developed code that makes it convenient to align these streams, by creating a new file that contains a single stream with all data points. TMSi has 
found accurate results for sample rates of 2048 Hz and lower, where the difference between synchronised data points remained within a single sample in 
15-minute recordings. For recordings made with sampling frequencies of 4000 or 4096 Hz, differences of a few samples (approximately 1ms) per 15 minutes 
are found. 

.. warning:: 

  TMSi stronly recommends to use the synchronization tool only for recordings that are made at sample rates of 2048 Hz or lower.