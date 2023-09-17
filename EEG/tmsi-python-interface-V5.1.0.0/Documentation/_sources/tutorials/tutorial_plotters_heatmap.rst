Tutorial 2: Heatmap plotter
==================================
*Corresponding file for this tutorial: TMSiHelpers/heatmap_plotter_helper.py*

The second example on plotter customization is the heatmap plotter. This tutorial focusses on the data acquisition part 
and providing the data to the heatmap; not on making the heatmap itself.

As the type of plotter is defined in the PlotterHelper-class, we have to make a new class named :mod:`HeatmapPlotterHelper`. 
We will derive this class from the :mod:`FilteredSignalPlotterHelper`, as we have to filter the data to remove DC offsets and 
signal drift before transferring Root Mean Square (RMS) values to a heatmap. Again, inheritance is used to base the new class on the parent class. 
The :meth:`__init__` method of the :mod:`FilteredSignalPlotterHelper` can be reused, where the :mod:`SignalPlotter` should be replaced by the :mod:`HeatmapPlotter`. 

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\heatmap_plotter_helper.py
    :language: python
    :lines: 51-57, 67

The :mod:`FilteredSignalPlotterHelper` and :mod:`SignalPlotterHelper` can be checked to see what changes are required to go from a signal plotter 
to a heatmap. Two changes are required: 

1. The callback function, which provides data to the plotter. 
2. The initialization where, instead of the different controls of the plotted channels, the locations of the electrodes have to be defined.

In the initialization a window length, over which the RMS is computed, needs to be defined. In addition, the initialization
of the heatmap has to be done here, which consists of setting the positions of the different electrodes.
The locations of the different electrodes depend on the selected grid or headcap. Those locations are provided in *TMSiFrontend*. 
The ordering of the channels differs between grids and can be read from the HD-grid configuration file (located in *TMSiSDK/tmsi_resources*). 
Channel locations, channels displayed in the heatmap and the reordering 
(if applicable) method have to be provided to the heatmap plotter to obtain the right positions and channel names.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\heatmap_plotter_helper.py
    :language: python
    :lines: 107-110

The callback function is the function that provides  data to the plotter. The callback is called with a response object. This response 
consists of a buffer object which consists of two parts. The object has a dataset that contains the data, and a pointer_buffer which is the pointer that controls where 
new data is added. The newest data is the data just before the pointer_buffer. For the heatmap, we should calculate the 
RMS-values over a specific time window, the calculation of which is shown in the snippet below. Next, the RMS is calculated and the data of
the channels present in the heatmap is sent to the plotter.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\heatmap_plotter_helper.py
    :language: python
    :lines: 76-92
