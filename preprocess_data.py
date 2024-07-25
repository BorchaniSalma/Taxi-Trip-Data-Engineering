import pandas as pd

# Path to the input .parquet file
input_file = 'data/yellow_tripdata_2022-01.parquet'

# Path to the output .csv file
output_file = 'data/yellow_tripdata_2022-01.csv'

# Read the parquet file
df = pd.read_parquet(input_file)

# Write the dataframe to a csv file
df.to_csv(output_file, index=False)

print(f"File successfully converted from {input_file} to {output_file}")
