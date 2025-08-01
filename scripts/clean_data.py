"""
This script is responsible for loading and cleaning the border crossing data.
It saves the cleaned data to the border_crossings_clean.csv file which is 
used for getting the aggregated data for analysis and plotting.

This script reads in the Border_Crossing_Data.csv file into a pandas data frame, 
processes it to clean and normalize the data, prepare it for aggregation, and then saves the cleaned data to 
border_crossings_clean.csv.

Things it does to the data:
 - Removes zero values and NaN values
 - Removes unnecessary columns ('Port Code', 'Latitude', 'Longitude', 'Point')
 - Normalize border names to 'Canada' and 'Mexico'
 - group by transportation measures: only group when they are from the same month, same border, and same port. 
    Example. sum values from calexico port from february 2025 from Personal vehicles + Personal Vehicle Passengers + Pedestrians
 -- Personal Transportation: Personal Vehicles + Personal Vehicle Passengers + Pedestrians
 -- Commercial Transportation: Trucks + Truck Containers (Loaded/Empty)
 -- Public Transportation: Buses + Bus Passengers
 -- Rail Transportation: Trains + Train Passengers + Rail Containers (Loaded/Empty)
 

Final Columns in the border_crossings_clean.csv file:
Port Name,State,Border,Date,Season,Measure,Value

"""
import pandas as pd
import os
from datetime import datetime
import logging

# Set up logging for professional data processing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_raw_data(file_path):
    """
    Load the raw border crossing data from CSV file.
    
    Args:
        file_path (str): Path to the raw CSV file
        
    Returns:
        pd.DataFrame: Raw border crossing data
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
    """
    logger.info(f"Loading raw data from: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")
    
    try:
        # Load the data with proper error handling
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        logger.info(f"Columns: {list(df.columns)}")
        return df
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The input file is empty")
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def remove_invalid_data(df):
    """
    Remove rows with zero values, NaN values, and invalid data.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with invalid data removed
    """
    logger.info("Removing invalid data (zeros, NaNs, negatives)")
    
    initial_rows = len(df)
    
    # Remove rows where Value is zero, NaN, or negative
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['Value'])  # Remove NaN values
    df_clean = df_clean[df_clean['Value'] > 0]    # Remove zero and negative values
    
    # Remove rows with missing essential information
    essential_columns = ['Port Name', 'Border', 'Date', 'Measure']
    df_clean = df_clean.dropna(subset=essential_columns)
    
    removed_rows = initial_rows - len(df_clean)
    logger.info(f"Removed {removed_rows} invalid rows ({removed_rows/initial_rows*100:.1f}%)")
    
    return df_clean


def remove_unnecessary_columns(df):
    """
    Remove columns that are not needed for analysis.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with unnecessary columns removed
    """
    logger.info("Removing unnecessary columns")
    
    # Columns to remove based on requirements
    columns_to_remove = ['Port Code', 'Latitude', 'Longitude', 'Point']
    
    # Only remove columns that actually exist in the dataframe
    existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]
    
    if existing_columns_to_remove:
        df_clean = df.drop(columns=existing_columns_to_remove)
        logger.info(f"Removed columns: {existing_columns_to_remove}")
    else:
        df_clean = df.copy()
        logger.info("No unnecessary columns found to remove")
    
    return df_clean


def normalize_border_names(df):
    """
    Normalize border names to consistent format.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with normalized border names
    """
    logger.info("Normalizing border names")
    
    df_clean = df.copy()
    
    # Create a mapping for border normalization
    border_mapping = {
        'US-Canada Border': 'Canada',
        'US-Mexico Border': 'Mexico'
    }
    
    # Apply the mapping
    df_clean['Border'] = df_clean['Border'].map(border_mapping)
    
    # Check if all borders were successfully mapped
    unmapped_borders = df_clean[df_clean['Border'].isna()]['Border'].unique()
    if len(unmapped_borders) > 0:
        logger.warning(f"Found unmapped border names: {unmapped_borders}")
    
    logger.info(f"Border distribution: {df_clean['Border'].value_counts().to_dict()}")
    
    return df_clean


def normalize_dates(df):
    """
    Convert date column to proper datetime format and add season information.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with normalized dates and season column
    """
    logger.info("Normalizing dates and adding season information")
    
    df_clean = df.copy()
    
    # Convert Date column to datetime
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='%b %Y')
    
    # Add season based on month
    def get_season(month):
        """Determine season based on month number."""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:  # months 9, 10, 11
            return 'Fall'
    
    df_clean['Season'] = df_clean['Date'].dt.month.apply(get_season)
    
    logger.info(f"Date range: {df_clean['Date'].min()} to {df_clean['Date'].max()}")
    logger.info(f"Season distribution: {df_clean['Season'].value_counts().to_dict()}")
    
    return df_clean


def categorize_transportation_measures(df):
    """
    Group transportation measures into four main categories and aggregate values.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with categorized transportation measures
    """
    logger.info("Categorizing transportation measures")
    
    # Define transportation categories based on requirements
    transportation_categories = {
        'Personal Transportation': [
            'Personal Vehicles', 
            'Personal Vehicle Passengers', 
            'Pedestrians'
        ],
        'Commercial Transportation': [
            'Trucks', 
            'Truck Containers Loaded', 
            'Truck Containers Empty'
        ],
        'Public Transportation': [
            'Buses', 
            'Bus Passengers'
        ],
        'Rail Transportation': [
            'Trains', 
            'Train Passengers', 
            'Rail Containers Loaded', 
            'Rail Containers Empty'
        ]
    }
    
    # Create reverse mapping from measure to category
    measure_to_category = {}
    for category, measures in transportation_categories.items():
        for measure in measures:
            measure_to_category[measure] = category
    
    df_clean = df.copy()
    
    # Map existing measures to categories
    df_clean['Transportation_Category'] = df_clean['Measure'].map(measure_to_category)
    
    # Check for unmapped measures
    unmapped_measures = df_clean[df_clean['Transportation_Category'].isna()]['Measure'].unique()
    if len(unmapped_measures) > 0:
        logger.warning(f"Found unmapped transportation measures: {unmapped_measures}")
        # For unmapped measures, keep original measure name
        df_clean['Transportation_Category'] = df_clean['Transportation_Category'].fillna(df_clean['Measure'])
    
    logger.info("Original measures distribution:")
    logger.info(df_clean['Measure'].value_counts().to_dict())
    
    # Aggregate values by grouping same transportation categories
    # Group by: Port Name, State, Border, Date, Season, Transportation_Category
    grouping_columns = ['Port Name', 'State', 'Border', 'Date', 'Season', 'Transportation_Category']
    df_aggregated = df_clean.groupby(grouping_columns)['Value'].sum().reset_index()
    
    # Rename Transportation_Category back to Measure for consistency
    df_aggregated = df_aggregated.rename(columns={'Transportation_Category': 'Measure'})
    
    logger.info(f"Aggregated from {len(df_clean)} to {len(df_aggregated)} rows")
    logger.info("Final transportation categories distribution:")
    logger.info(df_aggregated['Measure'].value_counts().to_dict())
    
    return df_aggregated


def save_cleaned_data(df, output_path):
    """
    Save the cleaned dataframe to CSV file.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe to save
        output_path (str): Path where to save the cleaned data
    """
    logger.info(f"Saving cleaned data to: {output_path}")
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    logger.info(f"Successfully saved {len(df)} rows to {output_path}")
    logger.info(f"Final columns: {list(df.columns)}")


def clean_data():
    """
    Main data cleaning function that can be imported and used by other scripts.
    
    Returns:
        pd.DataFrame: Cleaned border crossing data
    """
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    raw_data_path = os.path.join(project_root, 'data', 'raw', 'Border_Crossing_Data.csv')
    output_path = os.path.join(project_root, 'data', 'border_crossings_clean.csv')
    
    logger.info("Starting border crossing data cleaning pipeline")
    
    try:
        # Step 1: Load raw data
        df = load_raw_data(raw_data_path)
        
        # Step 2: Remove invalid data
        df = remove_invalid_data(df)
        
        # Step 3: Remove unnecessary columns
        df = remove_unnecessary_columns(df)
        
        # Step 4: Normalize border names
        df = normalize_border_names(df)
        
        # Step 5: Normalize dates and add seasons
        df = normalize_dates(df)
        
        # Step 6: Categorize and aggregate transportation measures
        df = categorize_transportation_measures(df)
        
        # Step 7: Save cleaned data
        save_cleaned_data(df, output_path)
        
        logger.info("Data cleaning pipeline completed successfully")
        return df
        
    except Exception as e:
        logger.error(f"Error in data cleaning pipeline: {str(e)}")
        raise


def main():
    """
    Main function that orchestrates the data processing pipeline.
    
    This function serves as the entry point when the script is run directly.
    It calls the clean_data function and handles any errors at the top level.
    """
    try:
        cleaned_df = clean_data()
        print(f"\nData cleaning completed successfully!")
        print(f"Cleaned dataset shape: {cleaned_df.shape}")
        print(f"Columns: {list(cleaned_df.columns)}")
        print(f"Date range: {cleaned_df['Date'].min()} to {cleaned_df['Date'].max()}")
        print(f"Borders: {cleaned_df['Border'].unique()}")
        print(f"Transportation measures: {cleaned_df['Measure'].unique()}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())