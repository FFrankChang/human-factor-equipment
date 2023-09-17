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
 * @file ${example_erp_analysis.py} 
 * @brief Example how to post process Poly5 data with MNE for evoked potentials. 
     Example is designed for an oddball experiment, but can be configured by user. 
 *
 */


'''

# Load packages
import sys
from os.path import join, dirname, realpath
Plugin_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Plugin_dir, '..', '..') # directory with all modules
measurements_dir = join(Plugin_dir, '../../measurements') # directory with all measurements
sys.path.append(modules_dir)
import mne
from mne.preprocessing import EOGRegression
from TMSiFileFormats.file_readers import Xdf_Reader
from IPython import get_ipython
import matplotlib.pyplot as plt
import numpy as np
from TMSiFileFormats.file_readers import Poly5Reader

ipython = get_ipython()
ipython.magic("matplotlib qt")


#%% Set variables by user

# Filter variables
fc_l = 1;           # Low pass cut-off frequency [Hz]
fc_h = 35           # High pass cut-off frequency [Hz]

# Event values
target_value = 64       # Stored value in TRIGGER channel for target stimulus
nontarget_value = 128   # Stored value in TRIGGER channel for nontarget stimulus

# Load data from Poly5 file
data = Poly5Reader()

# Sampling frequency [Hz]
fs = data.sample_rate

# Convert data to MNE object
mne_object = data.read_data_MNE()

# Poly5 dataformat cannot store the channeltypes. Therefore, the researcher should manually
# enter the types of data each channel holds. Channels are always ordered in the same way:
    # First channel is common reference, if enabled ('misc' channel)
    # all UNI channels that are enabled ('eeg' channels by default)
    # BIP channels (channel type depends on research)
    # TRIGGER channel ('misc' channel)
    # Status & counter channel ('misc' channels)

# Define channels in use (1 = enabled, 0 = disabled)
CREF_used = 1       # If measured with a common reference, set to 1,  otherwise 0
BIP1_used = 1       # If BIP channel 1 is used, set to 1, otherwise 0
BIP2_used = 1       # If BIP channel 2 is used, set to 1, otherwise 0
BIP3_used = 1       # If BIP channel 3 is used, set to 1, otherwise 0
BIP4_used = 1       # If BIP channel 4 is used, set to 1, otherwise 0
TRIGGER_used = 1    # If TRIGGER channel was enabled, set to 1, otherwise 0

# Fill out the number of EEG channels
number_eeg = 32

# Channel type for undefined channels
# Possible channel options include 'eog', 'eeg', 'ecg', 'emg', 'misc'
BIP1_type = 'eog'     # Signal type for BIP channel 1
BIP2_type = 'eog'     # Signal type for BIP channel 2
BIP3_type = 'ecg'     # Signal type for BIP channel 3
BIP4_type = 'emg'     # Signal type for BIP channel 4


# Define a variable for MNE that includes all channel types and all channels that are used in the correct order
channel_types = CREF_used * ['misc'] + number_eeg * ['eeg'] + BIP1_used * [BIP1_type] + BIP2_used * [BIP2_type] + BIP3_used * [BIP3_type] + BIP4_used * [BIP4_type] + TRIGGER_used * ['misc'] + 2 * ['misc']

# Create a new MNE object with all information based on the old MNE object
samples = mne_object._data
# Create the info for all channels
info_mne = mne.create_info(mne_object.ch_names, ch_types = channel_types, sfreq = fs)
# Add montage & electrode location information to the MNE object
info_mne.set_montage('standard_1020')
# Create the new object
mne_object = mne.io.RawArray(mne_object._data, info_mne)
# If a common reference is used, define reference
mne_object.set_eeg_reference(ref_channels = ['CREF'], ch_type = 'eeg')

#%%## Preprocessing

# Show data
mne_object.plot(title="Signal overview")

# Filter the data (high pass + lowpass)
preprocessed_data= mne_object.filter(l_freq=fc_l, h_freq=fc_h)

#%%## Retrieve epoched data

# Find the index of the TRIGGER channel (for APEX, change to STATUS to find stored triggers)
for i in range(len(mne_object.ch_names)):    
     if mne_object.ch_names[i] == 'TRIGGERS':
         trigger_chan_num = i

# Find the samples of the TRIGGER channel
trigger_chan_data = samples[trigger_chan_num]

# Find events in the data
preprocessed_data._data[trigger_chan_num] = trigger_chan_data
events = mne.find_events(preprocessed_data, stim_channel = 'TRIGGERS', output = 'onset')
event_dict = {'target stimulus': target_value, 'non-target stimulus': nontarget_value}

# Epoch data based on events found (-200 ms to +1000 ms)
epochs = mne.Epochs(preprocessed_data, events, event_id=event_dict, tmin=-0.2, tmax=1,
                    preload=True)

# Plotting arguments
plot_kwargs = dict(picks='all', ylim=dict(eeg=(-10, 10), eog=(-5, 15)))

# plot the evoked for the EEG and the EOG sensors
fig = epochs.average('all').plot(**plot_kwargs)
fig.set_size_inches(6, 6)

# Remove EOG artefacts with regression
model_plain = EOGRegression(picks='eeg', picks_artifact='eog').fit(epochs)
epochs_clean_plain = model_plain.apply(epochs)

# After regression, redo the baseline correction
epochs_clean_plain.apply_baseline()

# Show the evoked potential computed on the corrected data
plot_kwargs2 = dict(picks='all', ylim=dict(eeg=(-10, 10), eog=(-5, 15)))
fig = epochs_clean_plain.average('all').plot(**plot_kwargs)
fig.set_size_inches(6, 6)

# Average epochs per channel
erp_target =  epochs['target stimulus'].average()
erp_non_target =  epochs['non-target stimulus'].average()

# Plot the results per event
fig1 = erp_target.plot_joint(title="Average response target")
fig2 = erp_non_target.plot_joint(title= "Average response nontarget")

# plot the results for both events per location of electrode
fig5 = mne.viz.plot_evoked_topo([erp_target, erp_non_target],title = "Topological overview of responses to target and nontarget")
