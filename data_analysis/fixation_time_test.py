import pandas as pd

# Load the data
data_path = './data/Ma_eye_test.csv'
data = pd.read_csv(data_path)

# Convert 'StorageTime' to milliseconds
data['Timestamp_ms'] = data['StorageTime'] / 10000


# Define the rectangle coordinates (left, top, right, bottom)
rect_coords = (0, 0, 1920, 1080)

# Initialize variables for calculating total gaze time within the rectangle
total_gaze_time_ms = 0
previous_timestamp_ms = None

# Iterate through each row to check if the gaze is within the rectangle
for index, row in data.iterrows():
    x = row['fvo|ScreenPoint_x']
    y = row['fvo|ScreenPoint_y']
    current_timestamp_ms = row['Timestamp_ms']
    
    # Check if the gaze is inside the rectangle
    if rect_coords[0] <= x <= rect_coords[2] and rect_coords[1] <= y <= rect_coords[3]:
        if previous_timestamp_ms is not None:
            # Calculate the time difference from the previous timestamp
            time_diff_ms = current_timestamp_ms - previous_timestamp_ms
            total_gaze_time_ms += time_diff_ms
    
    # Update the previous timestamp
    previous_timestamp_ms = current_timestamp_ms

# Convert the total gaze time from milliseconds to seconds
total_gaze_time_seconds = total_gaze_time_ms / 1000

print(f"Total gaze time within the rectangle: {total_gaze_time_seconds} seconds")
