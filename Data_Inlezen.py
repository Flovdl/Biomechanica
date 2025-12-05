import pandas as pd
import requests
from io import BytesIO

def load_biomechanics_data_from_github(url):
    """
    Reads the raw biomechanics data from an Excel file hosted on GitHub, cleans the sheets,
    and consolidates the specified columns into a single DataFrame.

    Args:
        url (str): The raw URL to the Excel file on GitHub.

    Returns:
        pandas.DataFrame: The consolidated and cleaned DataFrame.
    """

    wanted_cols = [
        "ID",
        "Contact height (cm)",
        "Ball speed (m/s)",
        "Time (ms)",
        "Wrist speed",
        "Elbow speed",
        "Shoulder speed",
        "Ball speed"
    ]

    print(f"Loading data from GitHub URL: {url}")

    try:
        # Download the file content from GitHub
        response = requests.get(url)
        response.raise_for_status()  # Raise error if the download fails
        excel_file = BytesIO(response.content)
        
        # Read all sheets
        all_sheets = pd.read_excel(excel_file, sheet_name=None)
    except Exception as e:
        print(f"Error loading file from GitHub: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

    cleaned = []

    for sheet_name, sheet_df in all_sheets.items():
        # Clean column names
        sheet_df.columns = sheet_df.columns.str.strip()

        missing_cols = [col for col in wanted_cols if col not in sheet_df.columns]
        if missing_cols:
            print(f"Warning: Sheet '{sheet_name}' is missing columns: {missing_cols}. Skipping.")
            continue

        sheet_df = sheet_df.dropna(how="all")
        sheet_df = sheet_df[wanted_cols]
        sheet_df["Sheet_Name"] = sheet_name
        cleaned.append(sheet_df)

    if not cleaned:
        print("Error: No sheets were processed successfully.")
        return pd.DataFrame()

    df = pd.concat(cleaned, ignore_index=True)
    print(f"Successfully loaded and consolidated {len(cleaned)} sheets.")
    return df

# Example usage
if __name__ == "__main__":
    # Replace this with the **raw URL** of your Excel file on GitHub
    github_raw_url =  "https://raw.githubusercontent.com/Flovdl/Biomechanica/master/Volledige_Data_Set.xlsx"

    
    df = load_biomechanics_data_from_github(github_raw_url)
    if not df.empty:
        print("First 5 rows of the data:")
        print(df.head())
