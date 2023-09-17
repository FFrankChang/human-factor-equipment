.. _changes-page-label:

Changes from V4.1.0.0 to V5.1.0.0
===============================================

The TMSi Python Interface release V5.0.0.0 was a major release, introducing breaking changes with older versions of the TMSi Python Interface. 
Most changes are related to either the SAGA SDK, as this received a major overhaul to align with the APEX SDK. Another important change is the way that Plotters are provided.
This page describes the most important changes that you should be aware of, gives code snippets to highlight changes and refers to relevant additional documentation pages. 

APEX
---------------------------------

Device discovery
^^^^^^^^^^^^^^^^^^^^^^^^

The first change is related to device discovery, as the :meth:`TMSiSDK.discover() <TMSiSDK.tmsi_sdk.TMSiSDK.discover>` call now also allows the discovery of other device types. Therefore, an argument should be passed to the function, as outlined in the table below.

.. list-table:: APEX device discovery
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

          TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.usb)
          discoveryList = TMSiSDK().get_device_list()


     - .. code-block:: python

          TMSiSDK().discover(DeviceType.apex, DeviceInterfaceType.usb)
          discoveryList = TMSiSDK().get_device_list(DeviceType.apex)


Plotters
^^^^^^^^^^^^^^^^^^^^^^^^

Changes are made to the way plotters are handled. For a complete tutorial on how to use and edit these, please refer to :ref:`TMSi Plotter tutorial`. The way to use a plotter has changed as follows.

.. list-table:: APEX plotter use
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            # Initialise the plotter application
            app = QApplication(sys.argv)
        
            # Define the GUI object and show it
            plot_window = PlottingGUI(plotter_format = PlotterFormat.signal_viewer,
                                      figurename = 'A RealTimePlot', 
                                      device = dev)
            plot_window.show()
        
            # Enter the event loop
            app.exec_()

     - .. code-block:: python

            # Initialise the plotter application
            app = QApplication(sys.argv)

            # Initiate the plotter helper
            plotter_helper = SignalPlotterHelper(device = dev)

            # Define the GUI object and show it 
            gui = Gui(plotter_helper = plotter_helper)

            # Enter the event loop
            app.exec_()


SAGA
---------------------------------

The SAGA SDK has been changed so that it aligns with the structure set by the APEX SDK. The most important changes have been outlined in this section. 

Device discovery
^^^^^^^^^^^^^^^^^^^^^^^^

Discovery has changed, as explicit initialization of the SDK is not required anymore. 

.. list-table:: SAGA device discovery
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            tmsi_device.initialize()
    
            discoveryList = tmsi_device.discover(tmsi_device.DeviceType.saga, 
                                                 DeviceInterfaceType.docked, 
                                                 DeviceInterfaceType.usb)

     - .. code-block:: python

            TMSiSDK().discover(dev_type = DeviceType.saga, 
                               dr_interface = DeviceInterfaceType.docked, 
                               ds_interface = DeviceInterfaceType.usb)

            discoveryList = TMSiSDK().get_device_list(DeviceType.saga)


Device configuration
^^^^^^^^^^^^^^^^^^^^^^^^

Adapting the device configuration has changed significantly. For all specific configuration settings, the TMSiSDK now uses standardized “get” and “set” methods, per settable parameter. 
The table below lists a few examples (loading .xml-files, setting the (base) sample rate and changing the active channel list). 
For a complete list, please refer to the :mod:`SagaDevice <TMSiSDK.device.devices.saga.saga_device.SagaDevice>` API reference and the :ref:`different examples <examples-page-label>` that come with the TMSi Python Interface.

.. list-table:: SAGA device configuration
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            # Import device configuration from xml-file
            cfg = get_config("saga_config_EEG64")
            dev.load_config(cfg)

            # Changing the sampling rate of all channels to 2048 Hz
            dev.config.base_sample_rate = 4096
            dev.config.set_sample_rate(ChannelType.all_types, 2)

            # Changing the channel list to only include AUX channels
            ch_list = dev.config.channels
            for idx, ch in enumerate(ch_list):
                if (ch.type == ChannelType.AUX):
                    ch.enabled = True
                else :
                    ch.enabled = False
            dev.config.channels = ch_list


     - .. code-block:: python

            # Import device configuration from xml-file
            dev.import_configuration(join(configs_dir, "saga_config_EEG64.xml"))        

            # Changing the sampling rate of all channels to 2048 Hz
            dev.set_device_sampling_config(base_sample_rate = SagaBaseSampleRate.Binary)
            dev.set_device_sampling_config(channel_type = ChannelType.all_types, 
                                           channel_divider = 2)

            # Changing the channel list to only include AUX channels
            ch_list = dev.get_device_channels()
            enable_channels = []
            disable_channels = []
            for idx, ch in enumerate(ch_list):
                if (ch.get_channel_type() == ChannelType.AUX):
                    enable_channels.append(idx)
                else :
                    disable_channels.append(idx)
            dev.set_device_active_channels(enable_channels, True)
            dev.set_device_active_channels(disable_channels, False)


Channel properties
^^^^^^^^^^^^^^^^^^^^^^^^

Access to :mod:`Channel <TMSiSDK.device.tmsi_channel.TMSiChannel>` properties has also changed. In line with the device configuration, the different properties now employ a “get” and “set” method per property, wherever applicable. 
Please see the changes below.

.. list-table:: SAGA channel properties
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            ch_name = ch.name

            ch_unit_name = ch.unit_name

            ch_list = dev.config.channels

            for idx, ch in enumerate(ch_list):
                if idx == 1:
                    ch.name = "Fp1"
                if idx == 7:
                    ch.name = "F8"
            dev.config.channels = ch_list


     - .. code-block:: python

            ch_name = ch.get_channel_name()

            ch_unit_name = ch.get_channel_unit_name()

            dev.set_device_channel_names(["Fp1", "F8"], [1, 7])


Card configuration
^^^^^^^^^^^^^^^^^^^^^^^^

Some calls to configure SAGA’s SD card and retrieve data from the SD card have changed with respect to the previous version. The most important changes are listed in the table below. 
As can be seen in the code snippets, the card configuration method has changed to a more generic settable function in :meth:`set_card_recording_config() <TMSiSDK.device.devices.saga.saga_device.SagaDevice.set_card_recording_config>`. 
Rather than calling a specific method to start a card recording based on a button press, the method is now generalized where setting the button as start control is one of the parameters to set. 

.. list-table:: SAGA SD card configuration
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            # Retrieve active card configuration
            device_amb_conf = dev.get_device_memory_configuration()
            
            # Change the start control to button start. 
            # Rename file prefix to "Button"
            dev.set_device_recording_button("Button")

            # Retrieve the list of recordings available on SAGA
            recordings_list = dev.get_device_storage_list()
            if len(recordings_list) <= 0:
                raise(IndexError)
        
            # Download file from device 
            res = list(recordings_list.keys())[0]
            dev.download_recording_file(res)


     - .. code-block:: python

            # Retrieve active card configuration
            device_amb_conf = dev.get_card_recording_config()

            # Change the start control to button start. 
            # Rename file prefix to "ButtonRec"
            config = SagaStructureGenerator.create_card_record_configuration(
                device = dev,
                start_control = SagaEnums.SagaStartCardRecording.Button,
                prefix_file_name = "ButtonRec")
            dev.set_card_recording_config(config)

            # Retrieve the list of recordings available on SAGA
            recordings_list = dev.get_device_card_file_list()
            if len(recordings_list) <= 0:
                raise(IndexError)
                
            # Download file from device 
            dev.download_file_from_device(file_id= recordings_list[-1].RecFileID)


Plotters
^^^^^^^^^^^^^^^^^^^^^^^^

Changes are made to the way plotters are handled. For a complete tutorial on how to use and edit these, please refer to the :ref:`TMSi Plotter tutorial`. The way to use a plotter has changed as follows.

.. list-table:: SAGA plotter use
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            # Initialise the plotter application
            app = QApplication(sys.argv)
        
            # Define the GUI object and show it
            plot_window = PlottingGUI(plotter_format = PlotterFormat.signal_viewer,
                                      figurename = 'A RealTimePlot', 
                                      device = dev)
            plot_window.show()
        
            # Enter the event loop
            app.exec_()

     - .. code-block:: python

            # Initialise the plotter application
            app = QApplication(sys.argv)

            # Initiate the plotter helper
            plotter_helper = SignalPlotterHelper(device = dev)

            # Define the GUI object and show it 
            gui = Gui(plotter_helper = plotter_helper)

            # Enter the event loop
            app.exec_()

Interface type
^^^^^^^^^^^^^^^^^^^^^^^^

Changing SAGA’s communication interface between Data Recorder and Docking Station is now done by calling a general device :meth:`set() <TMSiSDK.device.devices.saga.saga_device.SagaDevice.set_device_interface>` method, 
rather than by accessing the “configuration” property of the device, which offered a method to change the communication interface.

.. list-table:: SAGA change communication interface
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            dev.config.set_interface_type(DeviceInterfaceType.wifi)

     - .. code-block:: python

            dev.set_device_interface(DeviceInterfaceType.wifi)

Start a measurement
^^^^^^^^^^^^^^^^^^^^^^^^

Starting a measurement now requires a :mod:`MeasurementType <TMSiSDK.device.tmsi_device_enums.MeasurementType>` Enum, where this was previously not 
strictly controlled. The sampling thread’s refresh time is now also a passable argument in :meth:`dev.start_measurement() <TMSiSDK.device.devices.saga.saga_device.SagaDevice.start_measurement>`. 
This argument allows for tweaking whether calls to SAGA should be made frequently (lower refresh time) or more infrequently (higher refresh time). 
Based on the processing requirements and available computation capacities of the PC, the value can be tweaked to your needs.

.. list-table:: SAGA measurement start
   :widths: 50 50
   :header-rows: 1

   * - V4.1.0.0
     - V5.1.0.0
   * - .. code-block:: python

            # Start a regular signal acquisition
            dev.start_measurement()

            # Start an impedance acquisition
            dev.start_measurement(MeasurementType.impedance)

     - .. code-block:: python

            # Start a regular signal acquisition
            dev.start_measurement(MeasurementType.SAGA_SIGNAL, 
                                  thread_refresh = 0.03)

            # Start an impedance acquisition
            dev.start_measurement(MeasurementType.SAGA_IMPEDANCE)
