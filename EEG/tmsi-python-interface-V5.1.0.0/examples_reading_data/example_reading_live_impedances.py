'''
(c) 2023 Twente Medical Systems International B.V., Oldenzaal The Netherlands

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#######  #     #   #####   #
   #     ##   ##  #        
   #     # # # #  #        #
   #     #  #  #   #####   #
   #     #     #        #  #
   #     #     #        #  #
   #     #     #  #####    #

/**
 * @file ${example_reading_live_impedances.py} 
 * @brief This example shows how to retrieve the saved impedances for APEX from a 
 * stored Poly5 datafile and plots the data for some channels
 */


'''
import sys
from os.path import join, dirname, realpath
Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)
import matplotlib.pyplot as plt
import numpy as np
from TMSiFileFormats.file_readers import Poly5Reader


# Channels of which impedance is of interest. In this example, the results of channel 1, channel 14 and channel 15 are plotted
idx_chan = [0,13,14]

# Load data from Poly5 file
data = Poly5Reader()
# Sampling frequency
fs = data.sample_rate
# Samples
samples = data.samples
# Channel names
chan_names = data.ch_names

# Define time variable for the plots
begin_time = 0
end_time = ((len(samples[1,:])-1)/fs)
time = np.linspace(0,end_time,len(samples[1,:]))

# Get the live impedances from the files. If the file does not have any live impedances, the array will be empty
# live_imp stores the impedance values as shown in the plotter
live_imp, _ = data.read_live_impedance()

# Show the live impedances
fig1,ax1 = plt.subplots()
ax1.plot(time,live_imp[idx_chan[0]])
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Impedance (kOhm)')
ax1.set_title(chan_names[idx_chan[0]])

# Example plot with a smaller y-range
fig2,ax2 = plt.subplots()
ax2.plot(time,live_imp[idx_chan[1]])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Impedance (kOhm)')
ax2.set_title(chan_names[idx_chan[1]])

fig3,ax3 = plt.subplots()
ax3.plot(time,live_imp[idx_chan[2]])
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Impedance (kOhm)')
ax3.set_title(chan_names[idx_chan[2]])




