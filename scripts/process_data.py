import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_raw_data(file_path):
    """
    Load raw border crossing data from CSV file.
    
    Parameters:
    file_path (str): Path to the raw CSV file
    
    Returns:
    pd.DataFrame: Raw data loaded from CSV
    """
    logger.info(f"Loading raw data from: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded {len(df)} records")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def clean_data_types(df):
    """
    Clean and convert data types for proper analysis.
    
    Parameters:
    df (pd.DataFrame): Raw dataframe
    
    Returns:
    pd.DataFrame: Dataframe with corrected data types
    """
    logger.info("Converting data types...")
    
    df_clean = df.copy()
    
    # Convert Date column to datetime with proper format
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], format='%b %Y')
    
    # Ensure Value column is numeric
    df_clean['Value'] = pd.to_numeric(df_clean['Value'], errors='coerce')
    
    # Convert Port Code to string (some may have leading zeros)
    df_clean['Port Code'] = df_clean['Port Code'].astype(str)
    
    # Strip whitespace from string columns
    string_columns = ['Port Name', 'State', 'Border', 'Measure']
    for col in string_columns:
        df_clean[col] = df_clean[col].astype(str).str.strip()
    
    logger.info("Data types converted successfully")
    return df_clean

def remove_unnecessary_columns(df):
    """
    Remove columns that are not needed for analysis.
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Dataframe with unnecessary columns removed
    """
    logger.info("Removing unnecessary columns...")
    
    columns_to_remove = ['Latitude', 'Longitude', 'Point']
    existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]
    
    if existing_columns_to_remove:
        df_clean = df.drop(columns=existing_columns_to_remove)
        logger.info(f"Removed columns: {existing_columns_to_remove}")
    else:
        df_clean = df.copy()
        logger.info("No unnecessary columns found to remove")
    
    return df_clean

def remove_null_and_zero_values(df):
    """
    Remove records with null values or zero crossing values.
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Dataframe with null and zero values removed
    """
    logger.info("Removing null and zero values...")
    
    initial_count = len(df)
    
    # Remove rows with null values
    df_clean = df.dropna()
    
    # Remove rows with zero or negative values (crossing counts should be positive)
    df_clean = df_clean[df_clean['Value'] > 0]
    
    final_count = len(df_clean)
    removed_count = initial_count - final_count
    
    logger.info(f"Removed {removed_count} records with null or zero values")
    logger.info(f"Remaining records: {final_count}")
    
    return df_clean

def normalize_border_names(df):
    """
    Normalize border column to simplified names.
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Dataframe with normalized border names
    """
    logger.info("Normalizing border names...")
    
    df_normalized = df.copy()
    
    # Create mapping for border names
    border_mapping = {
        'US-Canada Border': 'Canada',
        'US-Mexico Border': 'Mexico'
    }
    
    df_normalized['Border'] = df_normalized['Border'].map(border_mapping)
    
    # Verify all values were mapped
    unmapped_borders = df_normalized[df_normalized['Border'].isna()]['Border'].unique()
    if len(unmapped_borders) > 0:
        logger.warning(f"Unmapped border values found: {unmapped_borders}")
    
    logger.info("Border names normalized: US-Canada Border → Canada, US-Mexico Border → Mexico")
    return df_normalized

def normalize_transportation_measures(df):
    """
    Group and normalize transportation measures into logical categories.
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Dataframe with normalized and grouped measures
    """
    logger.info("Normalizing transportation measures...")
    
    # Create mapping for measure categories
    measure_mapping = {
        # Personal Transportation (combine vehicles and passengers)
        'Personal Vehicles': 'Personal Transportation',
        'Personal Vehicle Passengers': 'Personal Transportation',
        'Pedestrians': 'Personal Transportation',
        
        # Commercial Transportation (combine truck types)
        'Trucks': 'Commercial Transportation',
        'Truck Containers Loaded': 'Commercial Transportation', 
        'Truck Containers Empty': 'Commercial Transportation',
        
        # Public Transportation (combine bus types)
        'Buses': 'Public Transportation',
        'Bus Passengers': 'Public Transportation',
        
        # Rail Transportation (combine rail types)
        'Trains': 'Rail Transportation',
        'Train Passengers': 'Rail Transportation',
        'Rail Containers Loaded': 'Rail Transportation',
        'Rail Containers Empty': 'Rail Transportation'
    }
    
    df_normalized = df.copy()
    df_normalized['Measure_Category'] = df_normalized['Measure'].map(measure_mapping)
    
    # Check for unmapped measures
    unmapped_measures = df_normalized[df_normalized['Measure_Category'].isna()]['Measure'].unique()
    if len(unmapped_measures) > 0:
        logger.warning(f"Unmapped measures found: {unmapped_measures}")
        # Keep original measure for unmapped items
        df_normalized.loc[df_normalized['Measure_Category'].isna(), 'Measure_Category'] = df_normalized['Measure']
    
    logger.info("Transportation measures grouped into 4 main categories:")
    logger.info("- Personal Transportation (vehicles, passengers, pedestrians)")
    logger.info("- Commercial Transportation (trucks, containers)")
    logger.info("- Public Transportation (buses, bus passengers)")
    logger.info("- Rail Transportation (trains, rail containers, passengers)")
    
    return df_normalized

def aggregate_to_monthly_border_totals(df):
    """
    Aggregate to monthly totals by border and transportation type for easy plotting.
    
    Parameters:
    df (pd.DataFrame): Input dataframe with normalized measures
    
    Returns:
    pd.DataFrame: Monthly aggregated dataframe by border and transportation type
    """
    logger.info("Aggregating to monthly border totals by transportation type...")
    
    # Group by Date, Border, and Transportation Category - sum across all ports
    aggregation_columns = ['Date', 'Border', 'Measure_Category']
    
    df_aggregated = df.groupby(aggregation_columns).agg({
        'Value': 'sum'
    }).reset_index()
    
    # Rename the measure category column to measure for consistency
    df_aggregated = df_aggregated.rename(columns={'Measure_Category': 'Measure'})
    
    original_count = len(df)
    aggregated_count = len(df_aggregated)
    
    logger.info(f"Aggregated from {original_count} to {aggregated_count} monthly records")
    logger.info("Values summed by month, border, and transportation type across all ports")
    
    return df_aggregated

def add_derived_features(df):
    """
    Add minimal derived features needed for analysis.
    
    Parameters:
    df (pd.DataFrame): Input dataframe
    
    Returns:
    pd.DataFrame: Dataframe with month name for better readability
    """
    logger.info("Adding derived features...")
    
    df_enhanced = df.copy()
    
    # Add month name for better readability in plots
    df_enhanced['Month_Name'] = df_enhanced['Date'].dt.strftime('%B %Y')
    
    logger.info("Added derived features:")
    logger.info("- Month_Name for better plot readability")
    
    return df_enhanced

def validate_processed_data(df):
    """
    Validate the processed data for quality and consistency.
    
    Parameters:
    df (pd.DataFrame): Processed dataframe to validate
    
    Returns:
    bool: True if validation passes
    """
    logger.info("Validating processed data...")
    
    validation_errors = []
    
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        validation_errors.append(f"Missing values found: {missing_values[missing_values > 0].to_dict()}")
    
    # Check for negative values
    if (df['Value'] < 0).any():
        validation_errors.append("Negative values found in Value column")
    
    # Check for zero values (should have been removed)
    if (df['Value'] == 0).any():
        validation_errors.append("Zero values found in Value column")
    
    # Check for valid borders
    valid_borders = ['Canada', 'Mexico']
    invalid_borders = df[~df['Border'].isin(valid_borders)]['Border'].unique()
    if len(invalid_borders) > 0:
        validation_errors.append(f"Invalid border values: {invalid_borders}")
    
    # Check for valid measures
    valid_measures = ['Personal Transportation', 'Commercial Transportation', 
                     'Public Transportation', 'Rail Transportation']
    invalid_measures = df[~df['Measure'].isin(valid_measures)]['Measure'].unique()
    if len(invalid_measures) > 0:
        validation_errors.append(f"Invalid measure values: {invalid_measures}")
    
    if validation_errors:
        for error in validation_errors:
            logger.error(f"Validation error: {error}")
        return False
    else:
        logger.info("Data validation passed successfully")
        return True

def save_processed_data(df, output_path):
    """
    Save the processed dataframe to CSV file.
    
    Parameters:
    df (pd.DataFrame): Processed dataframe
    output_path (str): Path where to save the file
    """
    logger.info(f"Saving processed data to: {output_path}")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    logger.info(f"Successfully saved {len(df)} records to {output_path}")

def generate_processing_summary(original_df, processed_df):
    """
    Generate a summary of the data processing steps.
    
    Parameters:
    original_df (pd.DataFrame): Original raw dataframe
    processed_df (pd.DataFrame): Final processed dataframe
    """
    logger.info("\n" + "="*60)
    logger.info("DATA PROCESSING SUMMARY")
    logger.info("="*60)
    
    logger.info(f"Original records: {len(original_df):,}")
    logger.info(f"Processed records: {len(processed_df):,}")
    logger.info(f"Records removed: {len(original_df) - len(processed_df):,}")
    logger.info(f"Data reduction: {((len(original_df) - len(processed_df)) / len(original_df) * 100):.1f}%")
    
    logger.info(f"\nDate range: {processed_df['Date'].min().strftime('%B %Y')} to {processed_df['Date'].max().strftime('%B %Y')}")
    logger.info(f"Unique ports: {processed_df['Port Name'].nunique()}")
    logger.info(f"States covered: {processed_df['State'].nunique()}")
    logger.info(f"Transportation categories: {processed_df['Measure'].nunique()}")
    
    logger.info(f"\nBorder breakdown:")
    border_counts = processed_df['Border'].value_counts()
    for border, count in border_counts.items():
        print(f"  {border}: {count:,} records")
    
    logger.info(f"\nTransportation breakdown:")
    measure_counts = processed_df['Measure'].value_counts()
    for measure, count in measure_counts.items():
        print(f"  {measure}: {count:,} records")
    
    logger.info(f"\nTotal crossings: {processed_df['Value'].sum():,}")
    logger.info(f"Average crossings per record: {processed_df['Value'].mean():.0f}")

def main():
    """
    Main function that orchestrates the data processing pipeline.
    """
    start_time = datetime.now()
    logger.info("Starting border crossing data processing pipeline...")
    
    try:
        # Define file paths
        input_file = "../data/Border_Crossing_Data.csv"
        output_file = "../data/border_crossings_clean.csv"
        
        # Step 1: Load raw data
        raw_df = load_raw_data(input_file)
        
        # Step 2: Clean data types
        df = clean_data_types(raw_df)
        
        # Step 3: Remove unnecessary columns
        df = remove_unnecessary_columns(df)
        
        # Step 4: Remove null and zero values
        df = remove_null_and_zero_values(df)
        
        # Step 5: Normalize border names
        df = normalize_border_names(df)
        
        # Step 6: Normalize transportation measures
        df = normalize_transportation_measures(df)
        
        # Step 7: Aggregate to monthly border totals
        df = aggregate_to_monthly_border_totals(df)
        
        # Step 8: Add derived features
        df = add_derived_features(df)
        
        # Step 9: Validate processed data
        if not validate_processed_data(df):
            raise ValueError("Data validation failed")
        
        # Step 10: Save processed data
        save_processed_data(df, output_file)
        
        # Step 11: Generate summary
        generate_processing_summary(raw_df, df)
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"\n✓ Data processing pipeline completed successfully!")
        logger.info(f"Total processing time: {duration.total_seconds():.2f} seconds")
        
    except Exception as e:
        logger.error(f"❌ Error in data processing pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()