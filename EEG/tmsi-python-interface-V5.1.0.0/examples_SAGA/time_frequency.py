import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import xml.etree.ElementTree as ET
import keyboard
import time

def get_channel_names_from_info(info):
    """
    从LSL流的信息对象中解析通道名称，仅包括类型为EEG的通道。
    """
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        channel_type = channel.find('type').text
        if channel_type.upper() == 'EEG':
            channel_names.append(name)
        
    return channel_names

print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

inlet = StreamInlet(streams[0])
print("Stream found and connected.")

channel_names = get_channel_names_from_info(inlet.info())
sfreq = inlet.info().nominal_srate()
buffer = []

while True:
    if keyboard.is_pressed('esc'):
        print("Escape key pressed, exiting loop.")
        break

    sample, timestamp = inlet.pull_sample()
    if sample:
        buffer.append(sample[:-2])  # Assume last two channels are not EEG
        
        if len(buffer) >= int(sfreq * 4):  # Collect 4 seconds of data
            break
print(len(buffer))


# Prepare the data
data = np.array(buffer).T
ch_types = ['eeg'] * len(channel_names)
info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=ch_types)

# Create Raw object
raw = mne.io.RawArray(data, info)

# Apply band-pass filter
raw.filter(1, 40,fir_design='firwin')
print(raw.info)
# Plot the filtered data
# raw.plot(duration=2, n_channels=len(channel_names))

spectrum = raw.compute_psd(method='welch', fmin=1, fmax=40, n_jobs=1)

freqs = spectrum.freqs

alpha_band = (8, 12)
beta_band = (13, 30)

psd_data = spectrum.get_data()

power_alpha = np.zeros(len(raw.ch_names))
power_beta = np.zeros(len(raw.ch_names))

for i, ch_name in enumerate(raw.ch_names):
    alpha_indices = np.logical_and(freqs >= alpha_band[0], freqs <= alpha_band[1])
    beta_indices = np.logical_and(freqs >= beta_band[0], freqs <= beta_band[1])
    power_alpha[i] = np.mean(psd_data[i, alpha_indices])
    power_beta[i] = np.mean(psd_data[i, beta_indices])

for i, ch_name in enumerate(raw.ch_names):
    print(f'{ch_name}: α= {power_alpha[i]}, β = {power_beta[i]}')