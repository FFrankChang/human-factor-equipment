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
 * @file ${file_viewer.py} 
 * @brief This example loads files and opens them in a viewer 
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import tkinter as tk
from tkinter import filedialog
import matplotlib
import mne
import numpy as np
matplotlib.use('Qt5Agg')

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Poly5Reader, Xdf_Reader, Edf_Reader


root = tk.Tk()
filename = filedialog.askopenfilename(title = 'Select data file', filetypes = (('data-files', '*.poly5 .xdf .edf'),('All files', '*.*')))
root.withdraw()

mne_object =[]
try:
    if filename.lower().endswith('poly5'):
        data = Poly5Reader(filename)

        # Extract the samples and channel names from the Poly5Reader object
        samples = data.samples
        ch_names = data.ch_names
        
        # Conversion to MNE raw array
        mne_object = data.read_data_MNE() 

    elif filename.lower().endswith('xdf'):
        reader = Xdf_Reader(filename)
        mne_object, timestamps = reader.data, reader.time_stamps
        mne_object = mne_object[0]

    elif filename.lower().endswith('edf'):
        reader = Edf_Reader(filename)
        mne_object = reader.mne_object

    elif not filename:
        tk.messagebox.showerror(title='No file selected', message = 'No data file selected.')

    else:
        tk.messagebox.showerror(title='Could not open file', message = 'File format not supported. Could not open file.')


    if mne_object:
        # Retrieve the MNE RawArray info, channel names and sample data
        info_mne = mne_object.info
        ch_names = mne_object.info['ch_names']
        samples_mne = mne_object._data

        # Do not show not connected channels
        show_chs = []
        for idx, ch in enumerate(mne_object._data):
            if ch.any():
                show_chs = show_chs = np.hstack((show_chs,mne_object.info['ch_names'][idx]))
        data_object = mne_object.pick(show_chs)
        data_object.plot(scalings=dict(eeg = 250e-6), start= 0, duration = 5, n_channels = 5, title = filename, block = True) 

except:
    tk.messagebox.showerror(title='Could not open file', message = 'Something went wrong. Could not view file.')

    
    

