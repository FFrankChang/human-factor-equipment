import numpy as np
import mne
from pylsl import StreamInlet, resolve_stream
import xml.etree.ElementTree as ET
import keyboard

def get_channel_names_from_info(info):
    """
    从LSL流的信息对象中解析通道名称。
    """
    info_xml = info.as_xml()
    root = ET.fromstring(info_xml)
    channel_names = []
    
    for channel in root.find('desc').find('channels').findall('channel'):
        name = channel.find('label').text
        channel_names.append(name)
        
    return channel_names

def perform_time_frequency_analysis(data, sfreq, ch_names):
    ch_types = ['eeg'] * len(ch_names)  
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    
    raw = mne.io.RawArray(data, info)
    
    freqs = np.linspace(1, 40, 40)  # 1到40Hz
    n_cycles = freqs / 2.  # 每个频率的周期数
    power = mne.time_frequency.tfr_morlet(raw, freqs=freqs, n_cycles=n_cycles, return_itc=False)
    
    return power.data

print("Looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')

inlet = StreamInlet(streams[0])
print("Stream found and connected.")

channel_names = get_channel_names_from_info(inlet.info())

sfreq = inlet.info().nominal_srate()
buffer = []

while True:
    if keyboard.is_pressed('esc'):
        print("Escape key pressed, exiting loop")
        break

    # 从LSL流中拉取样本
    sample, timestamp = inlet.pull_sample()
    if sample:
        buffer.append(sample)
        print(sample)
        
        # 当缓冲区达到一定大小时进行时频分析
        if len(buffer) >= int(sfreq * 2):  # 以2秒数据进行一次分析
            data = np.array(buffer).T  # 转换为NumPy数组并转置以匹配(mne需要的channels, samples)
            result = perform_time_frequency_analysis(data, sfreq, channel_names)
            print("Time-frequency analysis done.")
            
            buffer = []  # 清空缓冲区
