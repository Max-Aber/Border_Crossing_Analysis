import pandas as pd

def load_and_clean_data(file_path):
    """
    Load the dataset and clean it by removing rows with null or zero values.
    
    Parameters:
    file_path (str): Path to the CSV file containing the border crossing data.
    
    Returns:
    pd.DataFrame: Cleaned DataFrame with null and zero entries removed.
    """
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # remove the lat, lon, and point columns as we are not using them, and are irrelevant to the analysis
    df = df.drop(["Latitude", "Longitude", "Point"], axis=1)
    
    # Convert 'Date' column to datetime format
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Remove null values and zero values
    df = df.dropna()
    df = df[df['Value'] > 0]
    
    return df