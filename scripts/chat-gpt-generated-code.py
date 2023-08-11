import os
import pandas as pd
from datetime import datetime

# Directory containing the CSV files
input_directory = "../local/input/"

# Get the current timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Output combined CSV file name with timestamp
output_file = f'combined_transactions_{timestamp}.csv'

# Initialize an empty list to store DataFrames
data_frames = []

# Iterate through each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        # Append the DataFrame to the list
        data_frames.append(df)

# Concatenate all DataFrames in the list
combined_data = pd.concat(data_frames, ignore_index=True)

# Save the combined data to the output file
combined_data.to_csv(output_file, index=False)

print(f"Combined {len(os.listdir(input_directory))} files into '{output_file}'.")