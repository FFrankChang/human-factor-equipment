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
 * @file ${example_ica.py} 
 * @brief Example how to post process Poly5 data with MNE ICA to remove EOG artefacts.
 */


'''

# Load packages
import sys
from os.path import join, dirname, realpath
import mne
from mne.preprocessing import (ICA, create_ecg_epochs,
                               create_eog_epochs)
from IPython import get_ipython
import pandas as pd
from matplotlib.pyplot import ion
ion() # enables interactive mode

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)
from TMSiFileFormats.file_readers import Poly5Reader

#%% load data and convert to mne object with correct properties

# Data can be downloaded from the TMSi site. Please download the ICA example data and select this file in the next step.
data = Poly5Reader()
raw = data.read_data_MNE() 

info = raw.info

# Poly5 dataformat cannot store the channeltypes and electrode locations. 
# Therefore, these should be updated.

# load channel locations from txt file
chLocs=pd.read_csv(join(modules_dir,'TMSiSDK/tmsi_resources/EEGchannelsTMSi3D.txt'), sep="\t", header=None)
chLocs.columns=['default_name', 'eeg_name', 'X', 'Y', 'Z']

# add locations and convert to head size of 95 mm
# change channel types of BIP channels
for idx, ch in enumerate(info['chs']):
    try:
        a=[i for i, e in (enumerate(chLocs['eeg_name'].values) or enumerate(chLocs['default_name'].values)) if e == ch['ch_name']]
        info['chs'][idx]['loc'][0]=95*1e-3*chLocs['X'].values[a]
        info['chs'][idx]['loc'][1]=95*1e-3*chLocs['Y'].values[a]
        info['chs'][idx]['loc'][2]=95*1e-3*chLocs['Z'].values[a]  
    except:
        if 'BIP 01' in ch['ch_name'] or 'BIP 02' in ch['ch_name']:
            raw.set_channel_types({ch['ch_name']: 'eog'})
        if 'BIP 03' in ch['ch_name']:
            raw.set_channel_types({ch['ch_name']: 'ecg'})
        if 'BIP 04' in ch['ch_name']:
            raw.set_channel_types({ch['ch_name']: 'emg'})


#%% Pre-process data

# Select relevant physiological data and crop data
raw.crop(tmax=40).pick_types(eeg=True, eog=True, ecg=True)

# Load and plot data
raw.load_data()
raw.plot(start=0, duration=40)

# High pass filter 
filt_raw = raw.copy().filter(l_freq=1., h_freq=None)

#%% Visualize the artefacts

# Epoch data based on EOG signal and show how channels are affected by EOG artefacts
eog_evoked = create_eog_epochs(raw).average()
eog_evoked.apply_baseline(baseline=(None, -0.2))
eog_evoked.plot_joint()

#%% Apply the ICA procedure 

# Apply the ICA procedure on the filtered data
# Use fixed random state to obtain identical results on every run
ica = ICA(n_components=20, max_iter='auto', random_state=97)
ica.fit(filt_raw)

# Plot ICA sources and components to analyse them by hand
ica.plot_sources(raw)
ica.plot_components()

# Based on visual inspection, manually exclude components 0 and 1 to remove EOG artefacts
ica.exclude = [0,1]

# Reconstruct original signals with artefacts removed and plot the results
reconstruct_raw = raw.copy()
ica.apply(reconstruct_raw)
reconstruct_raw.plot()

#%% Use EOG to select ICA components

# Reset components to exclude
ica.exclude = []

# find which ICs match the EOG pattern
eog_indices, eog_scores = ica.find_bads_eog(raw)
ica.exclude = eog_indices

# barplot of ICA component "EOG match" scores
ica.plot_scores(eog_scores)

# plot diagnostics
ica.plot_properties(raw, picks=eog_indices, psd_args=dict(fmax=60))

# plot ICs applied to raw data, with EOG matches highlighted
ica.plot_sources(raw)

# plot ICs applied to the averaged EOG epochs, with EOG matches highlighted
ica.plot_sources(eog_evoked)

# Reconstruct original signals with artefacts removed and plot the results
ica.apply(reconstruct_raw)
reconstruct_raw.plot(start=0, duration=40)


