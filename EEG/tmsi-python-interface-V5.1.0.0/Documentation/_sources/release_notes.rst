Release Notes V5.1.0.0
============================

**Release date: September 13th, 2023**

The current version (V5.1.0.0) of the TMSi Python Interface includes some new functionalities with respect to the previous version (V5.0.0.0). These changes include:

* Small bug fix for APEX configuration settings

Note that the V5.0.0.0 release was a **major release** and that the changes in SDK and plotters can include breaking changes for applications that were created 
using versions below V5.0.0.0 of the interface. Please learn about the changes :ref:`here <changes-page-label>`.


Previous release Notes
---------------------------------

V5.0.0.0
^^^^^^^^^^^^
**Release date: August 7th, 2023**

The current version (V5.0.0.0) of the TMSi Python Interface includes some new functionalities with respect to the previous version (V4.1.0.0). These changes include:

* Integrated APEX and SAGA control in one SDK, making it possible to control both devices in a similar way.
* Updated the plotters.
* Added new examples.
* Configurations should be device specific (ApexConfig or SagaConfig). The previous DeviceConfig is refused.

Note that the V5.0.0.0 release is a **major release** and that the changes in SDK and plotters can include breaking changes for applications that were created 
using previous versions of the interface. Please learn about the changes :ref:`here <changes-page-label>`.


V4.1.0.0
^^^^^^^^^^^^^^^^^^^^^^^^

**Release date: April 11th, 2023**

The current version (V4.1.0.0) of the TMSi Python interface includes some new 
functionalities with respect to the previous version (V4.0.0.0). These changes 
include:

* New installers to facilitate easy installation
* Added envelope plotter for EMG-signals.
* Reordering of data measured with HD-EMG grids is automatically applied in Poly5 and XDF reader, as well as during Poly5 to EDF conversion, when HD-EMG channel names are used.
* Examples for reading the data of different file formats are combined in example_file_viewer.py.
* XDF-file meta-data is updated to include the channels in reference.
* Added support for the USB-TTL module, so that it can be operated from the TMSi Python Interface directly.

V4.0.0.0
^^^^^^^^^^^^^^^^^^^^^

**Release date: December 19th, 2022**

The current version of the TMSi Python interface (V4.0.0.0) includes some new functionalities with respect to the previous version. These changes include:

* Added possibility for offline conversion of .Poly5 files to .EDF files and load this data to MNE, in both single fashion as well as batch conversion.
* Updated impedance plotter so that it can be used to disable channels which are suspected to give low-quality signals based on impedance values.
* Added support for new Textile HD-EMG grids layouts, both configuration files as well as updates of the plotters
* Initial release of the TMSi Python Interface for APEX


V3.0.0.0
^^^^^^^^^^^^^^

**Release date: July 29th, 2022**

The current version of the TMSi Python interface (V3.0.0.0) includes some new functionalities with respect to the previous version. These changes include:

Added functionality:

* Added possibility to synchronise data collected with LSL.
* Added an installation script to create a virtual environment with all required libraries.
* Added support for the Textile HD-EMG grids.
* Added Wi-Fi support, including back-up logging of data.
* Added support of card recordings, either to start as backup with a measurement, or by starting with a button press.

Improvements and changes:

* Re-work of the architecture to make it robust for future adaptations to the interface.
* Change to the way plotter objects are handled, refer to chapter 3 to see the changes. 
* Improved performance of the interface.
* Solved reported bug fixes posted on GitLab.


V2.0.0.0
^^^^^^^^^^^^^^^^^

**Release date: December 8th, 2021**

The current version (V2.0.0.0) of the TMSi Python interface includes some new functionalities with respect to the previous version. These changes include:

Added functionality:

* Added possibility to save data to the XDF file format
* Added possibility to save impedance values, both as .txt-file and included in an .XDF file
* Added LSL stream writer
* Added options to control the full device configuration
* Added an HD-EMG heatmap plotter

Improvements and changes:

* Improved performance of the interface
* Improved error handling of file-writer
* Improved performance of different plotters for different screen resolutions
* Changed handling of relative imports
* Changed location of configuration and location files
* Prepared plotter and examples for multi device experiments



V1.0.0.0
^^^^^^^^^^^^^

**Release date: June 10th, 2021**

* Initial release of the TMSi Python Interface for SAGA