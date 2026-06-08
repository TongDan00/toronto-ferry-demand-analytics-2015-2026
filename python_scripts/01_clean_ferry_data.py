import pandas as pd
import numpy as np

def clean_ferry_data(file_path):
    """
    Ingests, cleans, and engineers features for the Toronto Island Ferry dataset.
    """
    print("Loading raw data...")
    # load data
    df = pd.read_csv(file_path)
    print("Cleaning data and formatting timestamps...")

    # Drop unnecessary columns
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # Convert timestamp to datetime object
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Handle missing values (If there are intervals where the ferry was closed, counts might be NaN.)
  
    df['Redemption Count'] = df['Redemption Count'].fillna(0).astype(int)
    df['Sales Count'] = df['Sales Count'].fillna(0).astype(int)

    print("Engineering features for business dashboard...")
    # Time & date breakdowns
    df['Date'] = df['Timestamp'].dt.date
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month
    df['Hour'] = df['Timestamp'].dt.hour
    df['Minute'] = df['Timestamp'].dt.minute
    
    # Get the day of the week (Monday=1, Sunday=7) and map to names
    df['Day_of_Week_Num'] = df['Timestamp'].dt.dayofweek
    day_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
               4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['Day_of_Week'] = df['Day_of_Week_Num'].map(day_map)

    # Flag weekends (Saturday and Sunday)
    df['Is_Weekend'] = df['Day_of_Week_Num'].apply(lambda x: 1 if x >= 5 else 0)

    # Flag Off-Season (November through April)
    df['Is_Off_Season'] = df['Month'].apply(lambda x: 1 if x in [11, 12, 1, 2, 3, 4] else 0)

    # Calculate the rolling difference to spot bottlenecks
    df['Net_Queue_Change'] = df['Sales Count'] - df['Redemption Count']
    
    # Sort chronologically
    df = df.sort_values(by='Timestamp').reset_index(drop=True)

    print("Data cleaning complete.")
    return df

# Execution
if __name__ == "__main__":
    input_file = "/Users/yutong/Documents/code/git_test/toronto-ferry-demand-analytics-2015-2026/raw_data/Toronto Island Ferry Ticket Counts.csv" 
    output_file = "/Users/yutong/Documents/code/git_test/toronto-ferry-demand-analytics-2015-2026/CSV_for_analysis/toronto-ferry-cleaned_for_tableau.csv"
    
    # Run the pipeline
    cleaned_df = clean_ferry_data(input_file)
    
    # Preview the first few rows
    print("\nPreview of Cleaned Data:")
    print(cleaned_df[['Timestamp', 'Sales Count', 'Redemption Count', 'Hour', 'Is_Weekend', 'Net_Queue_Change']].head())
    
    # Save the transformed dataset
    cleaned_df.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved as: {output_file}")