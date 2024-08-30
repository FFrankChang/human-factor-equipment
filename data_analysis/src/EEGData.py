from scipy.signal import find_peaks,  butter, lfilter, welch
from Datafile import DataFile
import numpy as np
import pandas as pd

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

class EEGData(DataFile):
    def __init__(self, filepath, freq=1000):
        super().__init__(filepath)
        self.freq = freq
        self.convert_storage_time()
        self.calculate_heart_rate()  # Precompute heart rates

    def convert_storage_time(self):
        if 'timestamp_local' in self.data.columns:
            self.data.rename(columns={'timestamp_local': 'timestamp'}, inplace=True)
        else:
            print("StorageTime not found")

    def calculate_heart_rate(self):
        """Calculates heart rate from ECG data and calculates HRV RMSSD."""
        ecg_values = self.data['BIP 01'].values
        # Using distance=500 as half the frequency to ensure proper peak detection
        peaks, _ = find_peaks(ecg_values, distance=self.freq / 2)
        if len(peaks) > 1:
            rr_intervals = np.diff(peaks) / self.freq
            heart_rate = 60 / rr_intervals
            heart_rate_times = self.data['timestamp'].iloc[peaks][1:]  # Skipping the first peak because no interval before it

            # Calculate RMSSD
            rr_diff = np.diff(rr_intervals)
            rr_diff_squared = np.square(rr_diff)
            rmssd = np.sqrt(np.mean(rr_diff_squared))
            
            # Add RMSSD to each interval
            rmssd_values = [rmssd] * len(heart_rate)

            self.heart_rate_data = pd.DataFrame({
                'timestamp': heart_rate_times,
                'heart_rate': heart_rate,
                'HRV_RMSSD': rmssd_values
            })
        else:
            self.heart_rate_data = pd.DataFrame(columns=['timestamp', 'heart_rate', 'HRV_RMSSD'])
            print("Not enough peaks found to calculate heart rates and HRV")


    def extract_data_for_task(self, start_time, end_time, task_name):
        filtered_data = self.data[(self.data['timestamp'] >= start_time) & (self.data['timestamp'] <= end_time)].copy()
        if filtered_data.empty:
            print(f"{task_name} has no data")
            return None
        else:
            filtered_data.loc[:, '任务名称'] = task_name
            return filtered_data

    def get_average_heart_rate(self, extracted_data):
        """
        Gets the average heart rate for the duration covered by extracted_data.
        :param extracted_data: DataFrame containing data for a specific task with 'timestamp'.
        :return: float or None, the average heart rate over the specified timestamps.
        """
        if extracted_data is None or extracted_data.empty:
            print("No data available for average heart rate calculation")
            return None
        start_time = extracted_data['timestamp'].min()
        end_time = extracted_data['timestamp'].max()
        if not self.heart_rate_data.empty:
            relevant_heart_rates = self.heart_rate_data[(self.heart_rate_data['timestamp'] >= start_time) & (self.heart_rate_data['timestamp'] <= end_time)]
            if not relevant_heart_rates.empty:
                # Calculate and return the average heart rate
                average_heart_rate = relevant_heart_rates['heart_rate'].mean()
                if average_heart_rate < 10:
                    return None
                return average_heart_rate
            else:
                print("No heart rate data available for the specified interval")
                return None
        else:
            print("Heart rate data is not available")
            return None
        
    def get_average_rmssd(self, extracted_data):
        """
        Gets the average RMSSD for the duration covered by extracted_data.
        :param extracted_data: DataFrame containing data for a specific task with 'timestamp'.
        :return: float or None, the average RMSSD over the specified timestamps if data is available.
        """
        if extracted_data is None or extracted_data.empty:
            print("No data available for RMSSD calculation")
            return None
        
        # Get start and end time from extracted_data
        start_time = extracted_data['timestamp'].min()
        end_time = extracted_data['timestamp'].max()

        # Filter RMSSD data between these timestamps
        if not self.heart_rate_data.empty:
            relevant_rmssd = self.heart_rate_data[(self.heart_rate_data['timestamp'] >= start_time) & (self.heart_rate_data['timestamp'] <= end_time)]
            if not relevant_rmssd.empty:
                # Calculate the average RMSSD
                average_rmssd = relevant_rmssd['HRV_RMSSD'].mean()
                return average_rmssd
            else:
                print("No RMSSD data available for the specified interval")
                return None
        else:
            print("Heart rate data is not available")
            return None
        
    def calculate_relative_beta_power(self, extracted_data):
        channels = ["Fp1", "Fpz", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FC5", "FC1", "FC2", "FC6", "M1", "T7", "C3", "Cz", "C4", "T8", "M2", "CP5", "CP1", "CP2", "CP6", "P7", "P3", "Pz", "P4", "P8", "POz", "O1", "Oz", "O2"]
        beta_power = []

        for channel in channels:
            if channel in extracted_data.columns:
                filtered_data = bandpass_filter(extracted_data[channel], 1, 40, self.freq)

                freqs, psd = welch(filtered_data, self.freq, nperseg=1024)

                total_power = np.trapz(psd, freqs)
                beta_indices = (freqs >= 13) & (freqs <= 30)
                beta_power_specific = np.trapz(psd[beta_indices], freqs[beta_indices])

                relative_beta_power = beta_power_specific / total_power
                beta_power.append(relative_beta_power)
        if beta_power:
            average_beta_power = np.mean(beta_power)
            return average_beta_power
        else:
            return None