Tutorial 1: Filtered data plotter
=====================================
*Corresponding files for this tutorial: TMSiHelpers/filtered_signal_plotter_helper.py and examples_SAGA/example_filter_and_plot.py*

The first example on plotter customization is the filtered data plotter. Filtering data is best done on lower levels of the code, which happens in the 
:mod:`ConsumerThread`. This Thread is initialized and controlled by the :mod:`SignalPlotterHelper`. Therefore, new versions of both the :mod:`ConsumerThread` and the 
:mod:`PlotterHelper` have to be created. 

First, a new file should be created, where the classes :mod:`FilteredSignalPlotterHelper` and :mod:`FilteredConsumerThread` will be defined. 
The original classes should be imported and will be used for inheritance purposes. Inheritance allows new classes to reuse all methods
from the original classes and get the possibility to make the desired changes, see below. If you are not familiar with inheritance in programming, see 
‘https://www.youtube.com/watch?v=RSl87lqOXDE, Python OOP Tutorial 4: Inheritance - Creating Subclasses’ for some more information.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\filtered_signal_plotter_helper.py
    :language: python
    :lines: 39-41, 51, 84
 
The next step is to use the :mod:`FilteredConsumerThread` when using the :mod:`FilteredSignalPlotterHelper`. This is done by initializing the :mod:`FilteredConsumerThread` in 
the :mod:`FilteredSignalPlotter` instead of the original :mod:`ConsumerThread`.  To do so we will overwrite the :meth:`__init__` method of the :mod:`SignalPlotterHelper`. 
The original :meth:`__init__` of the :mod:`SignalPlotterHelper` calls the :meth:`__init__` of its parent class (:mod:`PlotterHelper`) with the :mod:`ConsumerThread` as argument. 
We want to overwrite this method and call the :meth:`__init__` of the parent class of the :mod:`SignalPlotterHelper` with the :mod:`FilteredConsumerThread` as argument. 
This is done using the :meth:`super()` method, which is highlighted in the code snippet below.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\filtered_signal_plotter_helper.py
    :language: python
    :lines: 51-55
    :emphasize-lines: 4

The file can be saved and the new class can be imported in the example file. Here, the :mod:`PlotterHelper` argument of the :mod:`Gui` can be changed 
to the newly created :mod:`FilteredSignalPlotterHelper`. 

.. literalinclude:: ..\..\..\examples_SAGA\example_filter_and_plot.py
    :language: python
    :lines: 51, 52, 82-84

After doing this, the application uses the :mod:`FilteredPlotterHelper` (which uses the :mod:`FilteredConsumerThread`). Next, the functional code of these two new classes can be modified and 
tailored to our wishes.

In the :mod:`FilteredConsumerThread` an additional buffer to store the filtered data is initialized. Furthermore, the filter itself should be initialized.
To do so, the method :meth:`initialize_filter` is created, which should be applied to the data in the :meth:`process` method, which needs to be overwritten for this 
purpose. The implementation of these methods can be found in the code.
To read out the filtered buffer instead of the original buffer, the monitor function is changed to return the filtered buffer.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\filtered_signal_plotter_helper.py
    :language: python
    :lines: 80-81

In order to control the filter, the desired filter settings need to be passed to the :mod:`FilteredSignalPlotterHelper` as arguments during initialization and stored for 
usage in the :mod:`FilteredConsumerThread`. 

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\filtered_signal_plotter_helper.py
    :language: python
    :lines: 51-60

The start method of the :mod:`FilteredSignalPlotterHelper` should be overwritten to initialize the filter. As this should be done between the different steps of 
the start function of the parent, the parent's start method can't be used. Therefore, the start method is overwritten completely and the initialization is done between 
the different steps.

.. literalinclude:: ..\..\..\TMSiPlotterHelpers\filtered_signal_plotter_helper.py
    :language: python
    :lines: 62-77
    :emphasize-lines: 8

Finally, the desired parameters (such as the filter's cut-off frequencies) are passed when calling the :mod:`FilteredSignalPlotterHelper` from the main script.



