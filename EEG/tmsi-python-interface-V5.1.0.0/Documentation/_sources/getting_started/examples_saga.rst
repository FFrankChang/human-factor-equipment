Examples SAGA
=================
With the examples you will be guided through the main features of the TMSi Python Interface. 
Connect a TMSi SAGA device to the PC and run the different examples. All SAGA examples use the USB and electrical (docked) interface as default interface types.


.. list-table:: 
    :widths: 30 70
    :header-rows: 0
    :stub-columns: 1

    * - Example bipolar and auxiliary measurement
      - This example shows the functionality to display the output of an AUX sensor and the output of a simultaneously sampled BIP channel on the screen. To do so, the channel configuration is updated and a call is made to update the sensor channels. The data is saved to a .Poly5 file.
    * - Example changing channel list
      - This example shows the manipulation of the active channel list and demonstrates how the channel names can be configured.
    * - Example changing reference method
      - This example shows how to change the :meth:`reference method <TMSiSDK.device.devices.saga.saga_API_enums.RefMethod>`. The configurable options are common reference (RefMethod.Common) and average reference (RefMethod.Average). When using common reference mode, :meth:`automatic switching <TMSiSDK.device.devices.saga.saga_API_enums.AutoRefMethod>` from common to average reference, in case the common reference electrode is out of range, can also be disabled or enabled. This can be configured using AutoRefMethod.Fixed and AutoRefMethod.Average.
    * - Example changing sample rate
      - This example shows how to change the :meth:`base sample rate <TMSiSDK.device.devices.saga.saga_API_enums.SagaBaseSampleRate>` of SAGA, as well as how the sample rate of individual channels can be changed.
    * - Example config settings
      - This example shows a brief overview of the different configuration settings of the SAGA device and how to change these settings. More elaborate explanations are given in the examples of the separate configuration items. 
    * - Example differential plot 
      - This example is designed for HD-EMG purposes and shows two plotters simultaneously. It shows the raw signals in the signal plotter and shows the single differential of the signals in the second plotter.
    * - Example EEG workflow
      - This example shows the functionality of the impedance plotter and the data stream plotter. The example is structured as if an EEG measurement is performed, so the impedance plotter is displayed in head layout. The channel names are set to the name convention of the TMSi EEG cap using a pre-configured EEG configuration. The data is saved to either the Poly5 or XDF file format, depending on user input.
    * - Example EMG workflow
      - This example shows the functionality of both the impedance plotter and the HD-EMG heatmap plotter. It is similar to the EEG example, but is modified for a HD-EMG workflow. The example shows the use with a Textile HD-EMG grid (4-8-L).
    * - Example envelope plot
      - This example shows how you can visualize the EMG envelope of the first BIP channel during acquisition. The filter is only applied to the plotter for displaying purposes, the saved data does not contain any filtered data.
    * - Example factory defaults
      - This example shows how to initiate a factory reset of the SAGA device.
    * - Example filter and plot
      - This example shows how to couple an additional signal processing object to the plotter. The application of a bandpass filter on the first 24 UNI channels is demonstrated. The filter is only applied to the plotter for displaying purposes, the saved data does not contain any filtered data.
    * - Example impedance plot
      - This example shows the functionality of the impedance plotter.
    * - Example load save configurations
      - This example shows how to load/save several different configurations from/to a file (in the “TMSiSDK/TMSi_resources” directory). 
    * - Example SD card configuration
      - This example shows the functionality to get and set the configuration of the onboard memory of SAGA. The prefix file name is changed in the example.
    * - Example SD card download
      - This example shows how to download card recordings that are stored on SAGA’s onboard memory. 
    * - Example SD card get list of files
      - This example shows how to retrieve all files that are currently stored on SAGA’s onboard memory. 
    * - Example stream LSL
      - This example shows how to set-up an LSL-stream for SAGA, which can be used in combination with other LSL applications.
    * - Example switch DR interface 
      - This example shows how to change the interface between SAGA's Docking Station and Data Recorder.
    * - Example WiFi measurement 
      - This example shows how to configure the wireless interface and how to perform a measurement over the wireless interface, where data is backed up to the SD card. Finally, the full recording is downloaded from the device.