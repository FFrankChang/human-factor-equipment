.. _TMSi Plotter tutorial:

Tutorial Plotters
=========================
From V5.0.0.0 onwards of the TMSi Python Interface, a new structure for the plotters is integrated. In this tutorial, a general outline of the plotter structure is
given. At the end of this page, you can find an :ref:`overview <customize-plotter-label>` of the step-by-step tutorials for specific plotters.

General structure
--------------------------
The new plotters have a new structure and are based on inheritance. A new class, the :mod:`Plotter Helper` class (after this called the :mod:`Helper`), has been developed in this version of the SDK.
The :mod:`Helper` class is a class where you can make your changes if you wish to have a different plotter from the ones delivered by default.

Globally, the structure of the new plotters is like this:

1. Top layer: The main file or example file that connects to the device, defines the device configuration and which :mod:`Helper` you will use. It calls the :mod:`GUI` with the correct :mod:`Helper` that defines which :mod:`Plotter` you will see.
2. Second layer: The :mod:`GUI` that opens the window for the :mod:`Plotter` and shows the correct :mod:`Plotter` based on the information given the :mod:`Helper` class.
3. Third layer: The :mod:`Helper` that has the ability to process the data, handles multiple plotters and defines which :mod:`Plotter` to use. This is the layer to adjust if you wish to customize your :mod:`Plotter`.
4. Fourth layer: The :mod:`Plotter`, that can edit what you can see from the data coming from the :mod:`Helper` (for example enabling/disabling the visibility of channels) and plots the data.

Looking at the layers, layer 1 and 3 can control the device, while layer 2 cannot. Layer 4 is a passive layer that can only do as desired by the layer 
above it. You can adjust the control of the device in layer 1 and customize what you want to display in layer 3.

In this tutorial, all layers will be explained one by one. Graphically, the structure explained above is summarized in Figure 1.

.. figure:: Overzicht_plotters.png
    :scale: 90%

    Figure 1: Overview of the general structure of the Plotters in the V5.0.0.0 release

Layer Overview
------------------------
In this paragraph, the role of every layer is explained in more detail. 

Top Layer: The main file or example file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The main file discovers and connects to the device. It can update the configuration of the device and open the filewriter to store data. It defines 
which :mod:`Helper` to use and initializes the :mod:`Helper`. Then, it executes the :mod:`GUI` using the :mod:`Helper`. When the :mod:`GUI` is closed by the user, the measurement is stopped and the filewriter and the connection
to the device is closed. This process is summarized in Figure 2.

.. figure:: Main_plotter_flow.png
    :scale: 20%

    Figure 2: Unified Modeling Language (UML) diagram of the main file

Second layer: The GUI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The :mod:`GUI` is the layer that opens the window for the :mod:`Plotter` and adds the :mod:`Plotter` to the window based on the :mod:`Helper`. It initializes and 
starts the :mod:`Helper` and closes it on the user's command. It does not have any interaction with the device.

Third layer: The Helper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The :mod:`Helper` contains the control of the device as well as the control of the reading of the data and the
processing of the data before it is sent to the :mod:`Plotter`. First, it initializes a :mod:`Consumer` and the :mod:`ConsumerThread`. The :mod:`Consumer` connects to the sample 
data server and puts the data in a queue. The :mod:`ConsumerThread` reads the queue and puts the data in a buffer. This :mod:`Buffer` is a circular buffer which is 
filled from start to end and then restarts from the beginning. The pointer keeps track of where the new data  is added.

After initializing and defining the :mod:`Consumer` and :mod:`ConsumerThread`, the :mod:`Helper` initializes the :mod:`Plotter` to be used and starts the data acquisition from the device.
Then, it initializes the :mod:`Monitor`. The :mod:`Monitor` outputs the data buffer to the :mod:`Helper` using the monitor function. The :mod:`Helper` receives the results of 
the monitor function in the callback function. The callback function receives, processes and sends the data to the :mod:`Plotter`. 

The workflow of the :mod:`Helper` is given in Figure 3. 

.. figure:: Helper_diagram_flow.png
    :scale: 20%

    Figure 3: Unified Modeling Language (UML) diagram of the :mod:`Helper` class

Fourth layer: The Plotter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The :mod:`Plotter` intializes the :mod:`Plotter` controls (for example, the autoscale button or enabled/disabled channels). It receives input
data from the :mod:`Helper` and processes and plots the data based on the controls. The :mod:`Plotter` does not have any interaction with the
device.

.. _customize-plotter-label:

How to customize your own plotter?
-----------------------------------
In case you want to change the :mod:`Helper`, there are a couple of points where you might want to make changes: the :meth:`callback` function or the 
:mod:`ConsumerThread` in combination with the monitor function. Any processing that can be done with the data buffer is suggested to be performed in the 
:meth:`callback` function (Tutorial 3), while processing that has to be done on a lower level is done is the :mod:`ConsumerThread` (see Tutorial 1).

For step-by-step guidance, please read through the following tutorials:

.. toctree::
   :titlesonly:

   tutorial_plotters_filtered
   tutorial_plotters_heatmap
   tutorial_plotters_differential


