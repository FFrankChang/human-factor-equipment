import pandas as pd

class DataFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            return pd.read_csv(self.filepath)
        except FileNotFoundError:
            print(f"{self.filepath} not found")
            return None
