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
 * @file ${file_reader.py} 
 * @brief This example loads files and shows how to retrieve the data from 
 * different file formats. The type of variables that are retrieved are the 
 * sampling frequency, samples, number of channels and channel names.
 *
 */


'''

import sys
from os.path import join, dirname, realpath
import tkinter as tk
from tkinter import filedialog
import matplotlib
import numpy as np

Example_dir = dirname(realpath(__file__)) # directory of this file
modules_dir = join(Example_dir, '..') # directory with all modules
measurements_dir = join(Example_dir, '../measurements') # directory with all measurements
sys.path.append(modules_dir)

from TMSiFileFormats.file_readers import Poly5Reader, Xdf_Reader, Edf_Reader

# Open the desired file
root = tk.Tk()
filename = filedialog.askopenfilename(title = 'Select data file', filetypes = (('data-files', '*.poly5 .xdf .edf'),('All files', '*.*')))
root.withdraw()

mne_object =[]
try:
    if filename.lower().endswith('poly5'):
        reader = Poly5Reader(filename)

        # Extract the samples and channel names from the Poly5Reader object
        samples = reader.samples
        ch_names = reader.ch_names
        sample_rate = reader.sample_rate
        num_channels = reader.num_channels

    elif filename.lower().endswith('xdf'):
        reader = Xdf_Reader(filename)
        data = reader.data[0]
        
        samples = data.get_data()
        ch_names = data.ch_names
        sample_rate = data.info['sfreq']
        num_channels = len(ch_names)

    elif filename.lower().endswith('edf'):
        reader = Edf_Reader(filename)
        data = reader.mne_object
        
        samples = data.get_data()
        ch_names = data.ch_names
        sample_rate = data.info['sfreq']
        num_channels = len(ch_names)

    elif not filename:
        tk.messagebox.showerror(title='No file selected', message = 'No data file selected.')

    else:
        tk.messagebox.showerror(title='Could not open file', message = 'File format not supported. Could not open file.')
    
    
    # Print retrieved data from the files
    print('Sample rate: ', sample_rate, ' Hz')
    print('Channel names: ', ch_names)
    print('Shape samples: ', np.shape(samples))

except:
    tk.messagebox.showerror(title='Could not open file', message = 'Something went wrong. Could not open file.')
