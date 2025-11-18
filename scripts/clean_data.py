"""
This script is responsible for loading and cleaning the border crossing data.
It creates separate CSV files for different types of measurements: people counts and vehicle counts.

This script reads in the Border_Crossing_Data.csv file into a pandas data frame, 
processes it to clean and normalize the data, and then saves separate cleaned datasets:
- border_crossings_people.csv: Contains only people measurements
- border_crossings_vehicles.csv: Contains only vehicle measurements  
- border_crossings_clean.csv: Contains all cleaned data (original format preserved)

Things it does to the data:
 - Removes NaN values and negative values (preserves legitimate zeros)
 - Removes unnecessary columns ('Port Code', 'Latitude', 'Longitude', 'Point')
 - Normalize border names to 'Canada' and 'Mexico'
 - Sorts data chronologically and groups by port for optimal analysis
 - Separates data by measurement type (people vs vehicles)
 - Standardizes measure names for consistency

Final output files:
1. border_crossings_people.csv - Columns: Port Name,State,Border,Date,Season,Measure,Value
   Where Measure is: Cars, Pedestrians, Buses, Trains (all representing people counts)

2. border_crossings_vehicles.csv - Columns: Port Name,State,Border,Date,Season,Measure,Value  
   Where Measure is: Cars, Trucks, Buses, Trains (all representing vehicle counts)

3. border_crossings_clean.csv - Original measures preserved for reference

Data is sorted chronologically (oldest first) and grouped by port for efficient analysis.
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
    Remove rows with invalid data while preserving legitimate zero values.
    
    Zero values are preserved as they may indicate:
    - Seasonal port closures
    - Policy-driven traffic changes  
    - Operational disruptions
    - Legitimate periods of no crossings
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with only invalid data removed
    """
    logger.info("Removing invalid data (NaNs, negatives) while preserving zeros")
    
    initial_rows = len(df)
    
    # Remove rows with invalid data but keep legitimate zeros
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=['Value'])     # Remove NaN values
    df_clean = df_clean[df_clean['Value'] >= 0]      # Remove negative values, keep zeros
    
    # Remove rows with missing essential information
    essential_columns = ['Port Name', 'Border', 'Date', 'Measure']
    df_clean = df_clean.dropna(subset=essential_columns)
    
    removed_rows = initial_rows - len(df_clean)
    zeros_preserved = (df_clean['Value'] == 0).sum()
    
    logger.info(f"Removed {removed_rows} invalid rows ({removed_rows/initial_rows*100:.1f}%)")
    logger.info(f"Preserved {zeros_preserved} legitimate zero values for analysis")
    
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


def sort_data_for_analysis(df):
    """
    Sort data chronologically and group by port for optimal analysis structure.
    
    This function organizes data to facilitate:
    - Time series analysis (chronological order)
    - Port-specific analysis (grouped by location)
    - Efficient data access patterns
    
    Sorting hierarchy:
    1. Date (chronological, oldest first)
    2. Port Name (alphabetical for consistency)  
    3. State (for ports with same names)
    4. Measure (for consistent grouping)
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Sorted dataframe optimized for analysis
    """
    logger.info("Sorting data chronologically and grouping by port")
    
    # Define sort order for optimal analysis
    sort_columns = ['Date', 'Port Name', 'State', 'Measure']
    
    # Sort data with multiple criteria
    df_sorted = df.sort_values(by=sort_columns, ascending=True).reset_index(drop=True)
    
    # Log sorting results for validation
    date_range = f"{df_sorted['Date'].min()} to {df_sorted['Date'].max()}"
    unique_ports = df_sorted['Port Name'].nunique()
    
    logger.info(f"Data sorted successfully:")
    logger.info(f"  • Date range: {date_range}")
    logger.info(f"  • {unique_ports} unique ports")
    logger.info(f"  • {len(df_sorted)} total records")
    
    return df_sorted


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


def create_people_dataset(df):
    """
    Create a dataset containing only people measurements with standardized measure names.
    
    This function filters the data to include only measurements that count people,
    not vehicles or containers. It standardizes the measure names for consistency.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe with all measures
        
    Returns:
        pd.DataFrame: Dataframe containing only people measurements
    """
    logger.info("Creating people dataset")
    
    # Define mapping from original measures to standardized people measures
    people_measure_mapping = {
        'Personal Vehicle Passengers': 'Cars',      # People traveling in cars
        'Pedestrians': 'Pedestrians',               # People walking
        'Bus Passengers': 'Buses',                  # People traveling in buses  
        'Train Passengers': 'Trains'                # People traveling in trains
    }
    
    # Filter data to include only people measurements
    people_measures = list(people_measure_mapping.keys())
    df_people = df[df['Measure'].isin(people_measures)].copy()
    
    # Standardize measure names
    df_people['Measure'] = df_people['Measure'].map(people_measure_mapping)
    
    logger.info(f"People dataset created with {len(df_people)} rows")
    logger.info(f"People measures distribution: {df_people['Measure'].value_counts().to_dict()}")
    
    return df_people


def create_vehicles_dataset(df):
    """
    Create a dataset containing only vehicle measurements with standardized measure names.
    
    This function filters the data to include only measurements that count vehicles,
    not people or containers. It standardizes the measure names for consistency.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe with all measures
        
    Returns:
        pd.DataFrame: Dataframe containing only vehicle measurements
    """
    logger.info("Creating vehicles dataset")
    
    # Define mapping from original measures to standardized vehicle measures
    vehicle_measure_mapping = {
        'Personal Vehicles': 'Cars',                # Personal vehicles/cars
        'Trucks': 'Trucks',                         # Commercial trucks
        'Buses': 'Buses',                           # Bus vehicles
        'Trains': 'Trains'                          # Train vehicles
    }
    
    # Filter data to include only vehicle measurements
    vehicle_measures = list(vehicle_measure_mapping.keys())
    df_vehicles = df[df['Measure'].isin(vehicle_measures)].copy()
    
    # Standardize measure names
    df_vehicles['Measure'] = df_vehicles['Measure'].map(vehicle_measure_mapping)
    
    logger.info(f"Vehicles dataset created with {len(df_vehicles)} rows")
    logger.info(f"Vehicle measures distribution: {df_vehicles['Measure'].value_counts().to_dict()}")
    
    return df_vehicles


def save_dataset(df, output_path, dataset_name):
    """
    Save a dataset to CSV file with proper logging and error handling.
    
    This function follows the Single Responsibility Principle by handling
    only the saving logic with comprehensive logging.
    
    Args:
        df (pd.DataFrame): Dataset to save
        output_path (str): Path where to save the file
        dataset_name (str): Human-readable name for logging
    """
    logger.info(f"Saving {dataset_name} to: {output_path}")
    
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    
    try:
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully saved {len(df)} rows to {output_path}")
        logger.info(f"Columns in {dataset_name}: {list(df.columns)}")
        
        # Log basic statistics for validation
        if 'Measure' in df.columns:
            logger.info(f"Measures in {dataset_name}: {df['Measure'].unique().tolist()}")
        
    except Exception as e:
        logger.error(f"Error saving {dataset_name}: {str(e)}")
        raise


def clean_data():
    """
    Main data cleaning function that creates separate datasets for people and vehicles.
    
    This function processes the raw border crossing data and creates three output files:
    1. People dataset - Contains only people measurements (passengers, pedestrians)
    2. Vehicles dataset - Contains only vehicle measurements (cars, trucks, buses, trains)
    3. Complete cleaned dataset - All measures preserved for reference
    
    Returns:
        tuple: (people_df, vehicles_df, complete_df) - All three cleaned datasets
    """
    # Define file paths following clean code principles
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Input path
    raw_data_path = os.path.join(project_root, 'data', 'raw', 'Border_Crossing_Data.csv')
    
    # Output paths (saving to processed folder)
    people_output_path = os.path.join(project_root, 'data', 'processed', 'border_crossings_people.csv')
    vehicles_output_path = os.path.join(project_root, 'data', 'processed', 'border_crossings_vehicles.csv')
    complete_output_path = os.path.join(project_root, 'data', 'processed', 'border_crossings_clean.csv')
    
    logger.info("Starting border crossing data cleaning pipeline")
    
    try:
        # Step 1: Load raw data
        df = load_raw_data(raw_data_path)
        
        # Step 2: Remove invalid data (NaNs, negatives) while preserving zeros
        df = remove_invalid_data(df)
        
        # Step 3: Remove unnecessary columns (Port Code, Lat, Lon, Point)
        df = remove_unnecessary_columns(df)
        
        # Step 4: Normalize border names (US-Canada -> Canada, US-Mexico -> Mexico)
        df = normalize_border_names(df)
        
        # Step 5: Normalize dates and add season information
        df = normalize_dates(df)
        
        # Step 6: Sort data chronologically and group by port
        df = sort_data_for_analysis(df)
        
        # Step 7: Create specialized datasets (maintaining sort order)
        people_df = create_people_dataset(df)
        vehicles_df = create_vehicles_dataset(df)
        
        # Step 8: Save all datasets
        save_dataset(people_df, people_output_path, "people dataset")
        save_dataset(vehicles_df, vehicles_output_path, "vehicles dataset") 
        save_dataset(df, complete_output_path, "complete cleaned dataset")
        
        logger.info("Data cleaning pipeline completed successfully")
        logger.info(f"Created {len(people_df)} people records and {len(vehicles_df)} vehicle records")
        
        return people_df, vehicles_df, df
        
    except Exception as e:
        logger.error(f"Error in data cleaning pipeline: {str(e)}")
        raise


def main():
    """
    Main function that orchestrates the data processing pipeline.
    
    This function serves as the entry point when the script is run directly.
    It calls the clean_data function and provides comprehensive reporting
    of the cleaning results to help users understand what was processed.
    """
    try:
        # Run the cleaning pipeline
        people_df, vehicles_df, complete_df = clean_data()
        
        # Report results to user
        print(f"\n" + "="*60)
        print("DATA CLEANING COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print(f"\nSUMMARY:")
        print(f"   • Complete dataset: {complete_df.shape[0]:,} rows")
        print(f"   • People dataset: {people_df.shape[0]:,} rows") 
        print(f"   • Vehicles dataset: {vehicles_df.shape[0]:,} rows")
        
        print(f"\nDATE RANGE:")
        print(f"   • From: {complete_df['Date'].min().strftime('%B %Y')}")
        print(f"   • To: {complete_df['Date'].max().strftime('%B %Y')}")
        
        print(f"\nBORDERS:")
        border_counts = complete_df['Border'].value_counts()
        for border, count in border_counts.items():
            print(f"   • {border}: {count:,} records")
        
        print(f"\nPEOPLE MEASUREMENTS:")
        people_measures = people_df['Measure'].value_counts()
        for measure, count in people_measures.items():
            print(f"   • {measure}: {count:,} records")
            
        print(f"\nVEHICLE MEASUREMENTS:")
        vehicle_measures = vehicles_df['Measure'].value_counts()
        for measure, count in vehicle_measures.items():
            print(f"   • {measure}: {count:,} records")
        
        print(f"\nOUTPUT FILES CREATED:")
        print(f"   • border_crossings_people.csv")
        print(f"   • border_crossings_vehicles.csv") 
        print(f"   • border_crossings_clean.csv")
        
        print(f"\nReady for analysis!")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        logger.error(f"Main function failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())