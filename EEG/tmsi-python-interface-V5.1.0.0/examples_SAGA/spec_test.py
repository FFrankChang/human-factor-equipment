
# from matplotlib import pyplot as plt
# from mne import set_log_level
# import keyboard
# import csv


# from mne_lsl.lsl import (
#     StreamInfo, StreamInlet, StreamOutlet, local_clock, resolve_streams
# )

# set_log_level("WARNING")
# streams = resolve_streams(name='SAGA')
# assert len(streams) == 1
# streams[0]
# inlet = StreamInlet(streams[0])
# inlet.open_stream()
# sinfo = inlet.get_sinfo()
# print(sinfo.get_channel_names())
# # time.sleep(0.01)
# with open('EEG_test.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     while True:
#         if keyboard.is_pressed('esc'):
#             print("Escape key pressed, exiting loop")
#             break
#         data, ts = inlet.pull_chunk()
#         writer.writerow([data,ts])
#         print(data,ts)
#     inlet.close_stream()
#     del inlet



# from pylsl import StreamInlet, resolve_stream
# streams = resolve_stream('name', 'SAGA')
# inlet = StreamInlet(streams[0])
# sinfo = inlet.info()
# print(sinfo.as_xml())
# inlet.close_stream()
# del inlet



import time

from matplotlib import pyplot as plt
from mne import set_log_level

from mne_lsl.datasets import sample
from mne_lsl.player import PlayerLSL as Player
from mne_lsl.stream import StreamLSL as Stream

stream = Stream(bufsize=2,name='SAGA').connect()
stream.pick("eeg")
stream.set_eeg_reference("Fpz")
print(stream.info)
picks = ("Fp1", "Fpz", "Fp2")  # channel selection
f, ax = plt.subplots(3, 1, sharex=True, constrained_layout=True)
for _ in range(3):  # acquire 3 separate window
    # figure how many new samples are available, in seconds
    winsize = stream.n_new_samples / stream.info["sfreq"]
    # retrieve and plot data
    data, ts = stream.get_data(winsize, picks=picks)
    for k, data_channel in enumerate(data):
        ax[k].plot(ts, data_channel)
    time.sleep(0.5)
for k, ch in enumerate(picks):
    ax[k].set_title(f"EEG {ch}")
ax[-1].set_xlabel("Timestamp (LSL time)")
plt.show()