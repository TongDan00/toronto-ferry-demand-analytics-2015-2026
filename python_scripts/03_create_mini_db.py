import pandas as pd
import os

source_csv_path = "CSV_for_analysis/toronto-ferry-cleaned_for_tableau.csv"
output_csv_path = "sample_database/sample_ferry_data.csv"

print(f"Reading data from {source_csv_path}...")

try:
    print("Extracting 1,000 rows...")
    sample_df = pd.read_csv(source_csv_path, nrows=1000)
    
    sample_df.to_csv(output_csv_path, index=False)
    
    file_size_mb = os.path.getsize(output_csv_path) / (1024 * 1024)
    print(f"Done. Sample CSV saved to {output_csv_path} ({file_size_mb:.2f} MB)")

except Exception as e:
    print(f"Script failed: {e}")