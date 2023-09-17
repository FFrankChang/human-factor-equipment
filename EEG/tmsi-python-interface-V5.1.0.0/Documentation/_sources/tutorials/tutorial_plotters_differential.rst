Tutorial 3: Differential plotter
==================================
*Corresponding file for this tutorial: TMSiHelpers/differential_signal_plotter_helper.py*

The next example outlines a differential signal viewer for HD-EMG purposes. The viewer displays the difference between 
successively separated grid electrodes (along the row direction). 

To be able to view both the unprocessed data and the single differentials data, two windows are initialized from the Gui. Here, the 
first window (with unprocessed data) is defined to be the main window. The class' close event is connected to this window. In the plotter helper,
a main plotter is defined using the :mod:`FilteredSignalPlotterHelper` and a secondary plotter is created using the :mod:`DifferentialSignalPlotterHelper`.
Both plotters are initialized similarly and receive the same data.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\differential_signal_plotter_helper.py
    :language: python
    :lines: 38-43

The single differentials can be calculated as a matrix multiplication between a pre-defined ‘single differential matrix’ and the data.
The single differential matrix and the differential names are determined based on channel names. See the code snippet for details on the implementation.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\differential_signal_plotter_helper.py
    :language: python
    :lines: 128-153

Once the channel names are known, the plotters can be constructed. The controls for both plotters are then based on each plotter's specific channel components.
In order to initialize the channel components, a list of channels needs to be passed, not just channel names. Therefore, the type of the channels' 
instance is needed. A second instance should be created, where the new channel names should be appended to the channel list:

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\differential_signal_plotter_helper.py
    :language: python
    :lines: 97-105

In order to be able to see the action potentials travel across the grid in the single differential mode, a short time range should be used.
Therefore, the time span of the differential plotter is set to 0.2s and the refresh rate is limited to 1 Hz, 
instead of the 10 Hz update frequency of the main plotter. 

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\differential_signal_plotter_helper.py
    :language: python
    :lines: 85-92

Rather than updating the plotted data in a cycling update, the newest data is now appended to the right side of the plot. As this differs for the signal plotter, 
a change needs to be made on how the processed data should be passed to the window. After updating this, the single differential calculation can be made and data can be provided to the plot.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\differential_signal_plotter_helper.py
    :language: python
    :lines: 67-83