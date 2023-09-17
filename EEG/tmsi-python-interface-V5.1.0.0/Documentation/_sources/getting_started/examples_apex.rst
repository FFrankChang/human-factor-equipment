Examples APEX
====================
The easiest way to start using the interface is to follow the examples. With the 
examples you will be guided through the main features of the TMSi Python Interface. 
Connect a TMSi APEX device to the PC and run the different examples. Except for 
the Bluetooth example, all examples use the USB interface as default interface type.


.. list-table:: 
    :widths: 30 70
    :header-rows: 0
    :stub-columns: 1

    * - Example bluetooth measurement
      - This example shows how to discover and connect to a device over the Bluetooth interface.
    * - Example card configuration
      - This example shows how to change the card recording configuration.
    * - Example change channel list
      - This example shows how to change which channels are included in the reference and shows how to change specific channel names.
    * - Example changing configuration
      - This example shows how to change the device sampling configuration. The example shows how to change the sampling frequency, disable the live-impedance measurement and set an impedance limit for the headcap indicator.
    * - Example config settings
      - This example shows how to load and save .xml configurations.
    * - Example EEG workflow 
      - This example shows the functionality of the impedance plotter and the data stream plotter. The example is structured as if an EEG measurement is performed, so the impedance plotter is displayed in head layout. The channel names are set to the name convention of the TMSi EEG cap using a pre-configured EEG configuration. The data is saved to either the .Poly5 or .XDF file format, depending on user input.
    * - Example factory defaults
      - This example shows how to initiate a factory reset of the device.
    * - Example filter and plot
      - This example shows how to connect an additional signal processing object to the plotter. The application of a bandpass filter on the CAP channels is demonstrated.
    * - Example impedance plot 
      - This example shows how to perform an impedance measurement and plot the data. The data can be saved to a .txt-file. 
    * - Example SD card download 
      - This example shows how to download card recordings that are stored on the onboard memory. 
    * - Example stream LSL
      - This example shows how to set-up an LSL-stream for APEX, which can be used in combination with other LSL applications.
