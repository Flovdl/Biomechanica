import pandas as pd
import os # Import os for better path handling

def load_biomechanics_data(file_path):
    """
    Reads the raw biomechanics data from an Excel file, cleans the sheets,
    and consolidates the specified columns into a single DataFrame.

    Args:
        file_path (str): The absolute path to the Raw_Data.xlsx file.

    Returns:
        pandas.DataFrame: The consolidated and cleaned DataFrame.
    """

    # Define the columns that we want to extract from each sheet
    wanted_cols = [
        "ID",
        "Contact hoogte",
        "Max(balsnelheid)(m/s)",
        "Time (ms)",
        "Wrist",
        "Elbow",
        "Shoulder",
        "Ball"
    ]

    print(f"Loading data from: {file_path}")

    try:
        # Read all sheets from the Excel file
        all_sheets = pd.read_excel(file_path, sheet_name=None)
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return pd.DataFrame() # Return an empty DataFrame on failure

    cleaned = []

    for sheet_name, sheet_df in all_sheets.items():
        
        # 1. Robust Column Cleaning: Strip leading/trailing whitespace
        sheet_df.columns = sheet_df.columns.str.strip()
        
        # Check if all wanted columns exist after cleaning
        # This prevents the KeyError if a column name is slightly wrong
        missing_cols = [col for col in wanted_cols if col not in sheet_df.columns]
        if missing_cols:
            print(f"Warning: Sheet '{sheet_name}' is missing columns: {missing_cols}. Skipping.")
            continue

        # 2. Remove rows that are completely empty
        sheet_df = sheet_df.dropna(how="all")

        # 3. Keep only your intended columns
        sheet_df = sheet_df[wanted_cols]

        # 4. Add sheet name (spike session identifier)
        sheet_df["Sheet_Name"] = sheet_name

        cleaned.append(sheet_df)
    
    if not cleaned:
        print("Error: No data sheets were processed successfully.")
        return pd.DataFrame()

    # 5. Combine all cleaned sheets into one final DataFrame
    df = pd.concat(cleaned, ignore_index=True)
    
    print(f"Successfully loaded and consolidated {len(cleaned)} sheets.")
    return df

# Example of how you can test this module by running it directly (optional block)
if __name__ == '__main__':
    # NOTE: You MUST replace this path with your actual file location 
    # for local testing, or comment out the block.
    test_file_path = r"C:\Users\Florian\PycharmProjects\Applied_biomechanics\Raw_Data.xlsx"
    
    # Check if the file exists before attempting to load
    if os.path.exists(test_file_path):
        test_df = load_biomechanics_data(test_file_path)
        if not test_df.empty:
            print("\nTest Load Successful. First 5 rows of data:")
            print(test_df.head())
    else:
        print(f"Test File Missing. Please update the path in data_loader.py if running directly: {test_file_path}")