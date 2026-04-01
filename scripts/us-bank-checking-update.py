import pandas as pd
from datetime import datetime
import os
import logging

# Change this to your actual CSV file path

input_file = 'Checking - 2977_01-01-2020_07-02-2025.csv'
localInput = '../local/input/' + input_file
output_file = 'updated-' + input_file
localOutput = '../local/output/' + output_file
logging.critical(os.path.basename(input_file))
# output_file = '../local/output/updated_' + input_file

# Read the CSV into a DataFrame
df = pd.read_csv(localInput)

# Ensure Date column is parsed as datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Extract Year and Month
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month.apply(lambda x: f'{x:02d}')  # Two-digit month

# Write to a new CSV
df.to_csv(localOutput, index=False)

print(f"Updated file saved as: {localOutput}")
