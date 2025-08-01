"""
This script is responsible for making the aggregated csv for analysis and plotting.
It reads the cleaned data from border_crossings_clean.csv and saves the aggregated 
data in seperate csv files. The following files are created:
 - monthly_crossings.csv          # Aggregated monthly data for total trends
 - seasonal_crossings.csv         # Data grouped by season (Winter/Spring/Summer/Fall)
 - measure_crossings.csv          # Aggregated monthly by crossing type
 - border_region_crossings.csv    # Aggregated monthly by US-MX/US-CAN border
 - top_ports_crossings_2000s.csv  # Total Crossings by ports since Jan 2000
"""
import pandas as pd
import os
import logging
from datetime import datetime

# Set up logging for professional data processing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_cleaned_data(file_path):
    """
    Load the cleaned border crossing data from CSV file.
    
    Args:
        file_path (str): Path to the cleaned CSV file
        
    Returns:
        pd.DataFrame: Cleaned border crossing data ready for aggregation
        
    Raises:
        FileNotFoundError: If the cleaned data file doesn't exist
        ValueError: If required columns are missing
    """
    logger.info(f"Loading cleaned data from: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cleaned data file not found: {file_path}")
    
    try:
        # Load the cleaned data
        df = pd.read_csv(file_path)
        
        # Validate required columns exist
        required_columns = ['Port Name', 'State', 'Border', 'Date', 'Season', 'Measure', 'Value']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Convert Date column to datetime for proper sorting and filtering
        df['Date'] = pd.to_datetime(df['Date'])
        
        logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        logger.info(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        logger.info(f"Borders: {df['Border'].unique()}")
        logger.info(f"Transportation measures: {df['Measure'].unique()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading cleaned data: {str(e)}")
        raise


def create_monthly_aggregation(df):
    """
    Create monthly aggregation of all border crossings for total trend analysis.
    
    This aggregates all transportation types and ports by month to show
    overall border crossing trends over time.
    
    Args:
        df (pd.DataFrame): Cleaned border crossing data
        
    Returns:
        pd.DataFrame: Monthly aggregated data with columns: Date, Total_Crossings
    """
    logger.info("Creating monthly aggregation for total trends")
    
    # Group by Date (month) and sum all crossings
    monthly_df = df.groupby('Date')['Value'].sum().reset_index()
    monthly_df = monthly_df.rename(columns={'Value': 'Total_Crossings'})
    
    # Sort by date for proper time series
    monthly_df = monthly_df.sort_values('Date')
    
    # Add additional time-based columns for analysis
    monthly_df['Year'] = monthly_df['Date'].dt.year
    monthly_df['Month'] = monthly_df['Date'].dt.month
    monthly_df['Month_Name'] = monthly_df['Date'].dt.strftime('%B')
    
    logger.info(f"Created monthly aggregation with {len(monthly_df)} months")
    logger.info(f"Total crossings range: {monthly_df['Total_Crossings'].min():,} to {monthly_df['Total_Crossings'].max():,}")
    
    return monthly_df


def create_seasonal_aggregation(df):
    """
    Create seasonal aggregation showing average crossings by season.
    
    This groups data by season (Winter, Spring, Summer, Fall) and calculates
    average monthly crossings for each season across all years.
    
    Args:
        df (pd.DataFrame): Cleaned border crossing data
        
    Returns:
        pd.DataFrame: Seasonal aggregated data with columns: Season, Avg_Monthly_Crossings, Total_Crossings
    """
    logger.info("Creating seasonal aggregation")
    
    # First, get monthly totals by season and year for proper averaging
    monthly_seasonal = df.groupby(['Date', 'Season'])['Value'].sum().reset_index()
    monthly_seasonal = monthly_seasonal.rename(columns={'Value': 'Monthly_Total'})
    
    # Then calculate average monthly crossings per season across all years
    seasonal_df = monthly_seasonal.groupby('Season').agg({
        'Monthly_Total': ['mean', 'sum', 'count', 'std']
    }).round(0)
    
    # Flatten column names
    seasonal_df.columns = ['Avg_Monthly_Crossings', 'Total_Crossings', 'Month_Count', 'Std_Deviation']
    seasonal_df = seasonal_df.reset_index()
    
    # Order seasons logically: Winter, Spring, Summer, Fall
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    seasonal_df['Season'] = pd.Categorical(seasonal_df['Season'], categories=season_order, ordered=True)
    seasonal_df = seasonal_df.sort_values('Season')
    
    logger.info(f"Created seasonal aggregation with {len(seasonal_df)} seasons")
    logger.info("Seasonal distribution:")
    for _, row in seasonal_df.iterrows():
        logger.info(f"  {row['Season']}: Avg {row['Avg_Monthly_Crossings']:,.0f} crossings/month")
    
    return seasonal_df


def create_measure_aggregation(df):
    """
    Create monthly aggregation by transportation measure (crossing type).
    
    This shows monthly trends for each transportation category:
    Personal, Commercial, Public, and Rail Transportation.
    
    Args:
        df (pd.DataFrame): Cleaned border crossing data
        
    Returns:
        pd.DataFrame: Monthly data by measure with columns: Date, Measure, Monthly_Crossings
    """
    logger.info("Creating transportation measure aggregation")
    
    # Group by Date and Measure to get monthly totals by transportation type
    measure_df = df.groupby(['Date', 'Measure'])['Value'].sum().reset_index()
    measure_df = measure_df.rename(columns={'Value': 'Monthly_Crossings'})
    
    # Sort by date and measure for proper organization
    measure_df = measure_df.sort_values(['Date', 'Measure'])
    
    # Add time-based columns for easier analysis
    measure_df['Year'] = measure_df['Date'].dt.year
    measure_df['Month'] = measure_df['Date'].dt.month
    measure_df['Month_Name'] = measure_df['Date'].dt.strftime('%B')
    
    logger.info(f"Created measure aggregation with {len(measure_df)} records")
    
    # Log distribution by transportation type
    measure_totals = measure_df.groupby('Measure')['Monthly_Crossings'].sum().sort_values(ascending=False)
    logger.info("Transportation measure totals:")
    for measure, total in measure_totals.items():
        logger.info(f"  {measure}: {total:,} total crossings")
    
    return measure_df


def create_border_region_aggregation(df):
    """
    Create monthly aggregation by border region (Canada vs Mexico).
    
    This compares monthly crossing patterns between US-Canada and US-Mexico borders.
    
    Args:
        df (pd.DataFrame): Cleaned border crossing data
        
    Returns:
        pd.DataFrame: Monthly data by border with columns: Date, Border, Monthly_Crossings
    """
    logger.info("Creating border region aggregation")
    
    # Group by Date and Border to get monthly totals by border region
    border_df = df.groupby(['Date', 'Border'])['Value'].sum().reset_index()
    border_df = border_df.rename(columns={'Value': 'Monthly_Crossings'})
    
    # Sort by date and border for proper organization
    border_df = border_df.sort_values(['Date', 'Border'])
    
    # Add time-based columns for easier analysis
    border_df['Year'] = border_df['Date'].dt.year
    border_df['Month'] = border_df['Date'].dt.month
    border_df['Month_Name'] = border_df['Date'].dt.strftime('%B')
    
    logger.info(f"Created border region aggregation with {len(border_df)} records")
    
    # Log distribution by border
    border_totals = border_df.groupby('Border')['Monthly_Crossings'].sum().sort_values(ascending=False)
    logger.info("Border region totals:")
    for border, total in border_totals.items():
        logger.info(f"  {border}: {total:,} total crossings")
    
    return border_df


def create_top_ports_aggregation(df):
    """
    Create aggregation of top ports by total crossings since January 2000.
    
    This identifies the busiest border crossing ports for focused analysis.
    
    Args:
        df (pd.DataFrame): Cleaned border crossing data
        
    Returns:
        pd.DataFrame: Top ports data with columns: Port Name, State, Border, Total_Crossings, Avg_Monthly_Crossings
    """
    logger.info("Creating top ports aggregation since 2000")
    
    # Filter data from January 2000 onwards
    df_2000s = df[df['Date'] >= '2000-01-01'].copy()
    
    if len(df_2000s) == 0:
        logger.warning("No data found from 2000 onwards")
        return pd.DataFrame()
    
    logger.info(f"Analyzing {len(df_2000s)} records from {df_2000s['Date'].min()} to {df_2000s['Date'].max()}")
    
    # Group by port information and calculate total crossings
    port_columns = ['Port Name', 'State', 'Border']
    ports_df = df_2000s.groupby(port_columns).agg({
        'Value': ['sum', 'mean', 'count'],
        'Date': ['min', 'max']
    }).round(0)
    
    # Flatten column names
    ports_df.columns = ['Total_Crossings', 'Avg_Monthly_Crossings', 'Month_Count', 'First_Record', 'Last_Record']
    ports_df = ports_df.reset_index()
    
    # Sort by total crossings (busiest ports first)
    ports_df = ports_df.sort_values('Total_Crossings', ascending=False)
    
    # Add ranking
    ports_df['Rank'] = range(1, len(ports_df) + 1)
    
    # Reorder columns for better readability
    column_order = ['Rank', 'Port Name', 'State', 'Border', 'Total_Crossings', 
                   'Avg_Monthly_Crossings', 'Month_Count', 'First_Record', 'Last_Record']
    ports_df = ports_df[column_order]
    
    logger.info(f"Created top ports aggregation with {len(ports_df)} ports")
    logger.info("Top 10 busiest ports:")
    for _, row in ports_df.head(10).iterrows():
        logger.info(f"  {row['Rank']}. {row['Port Name']}, {row['State']} ({row['Border']}): {row['Total_Crossings']:,.0f} crossings")
    
    return ports_df


def save_aggregated_data(df, filename, output_dir):
    """
    Save aggregated dataframe to CSV file in the processed directory.
    
    Args:
        df (pd.DataFrame): Dataframe to save
        filename (str): Name of the output file (without path)
        output_dir (str): Directory where to save the file
    """
    if df.empty:
        logger.warning(f"Empty dataframe for {filename}, skipping save")
        return
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    
    # Create full file path
    output_path = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    logger.info(f"Saved {len(df)} rows to {output_path}")


def aggregate_data():
    """
    Main data aggregation function that can be imported and used by other scripts.
    
    This function orchestrates the creation of all aggregated datasets from
    the cleaned border crossing data.
    
    Returns:
        dict: Dictionary containing all aggregated dataframes
    """
    # Define file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    cleaned_data_path = os.path.join(project_root, 'data', 'border_crossings_clean.csv')
    processed_dir = os.path.join(project_root, 'data', 'processed')
    
    logger.info("Starting border crossing data aggregation pipeline")
    
    try:
        # Step 1: Load cleaned data
        df = load_cleaned_data(cleaned_data_path)
        
        # Step 2: Create monthly aggregation for total trends
        monthly_df = create_monthly_aggregation(df)
        save_aggregated_data(monthly_df, 'monthly_crossings.csv', processed_dir)
        
        # Step 3: Create seasonal aggregation
        seasonal_df = create_seasonal_aggregation(df)
        save_aggregated_data(seasonal_df, 'seasonal_crossings.csv', processed_dir)
        
        # Step 4: Create transportation measure aggregation
        measure_df = create_measure_aggregation(df)
        save_aggregated_data(measure_df, 'measure_crossings.csv', processed_dir)
        
        # Step 5: Create border region aggregation
        border_df = create_border_region_aggregation(df)
        save_aggregated_data(border_df, 'border_region_crossings.csv', processed_dir)
        
        # Step 6: Create top ports aggregation
        ports_df = create_top_ports_aggregation(df)
        save_aggregated_data(ports_df, 'top_ports_crossings_2000s.csv', processed_dir)
        
        logger.info("Data aggregation pipeline completed successfully")
        
        # Return all aggregated datasets for potential further use
        return {
            'monthly': monthly_df,
            'seasonal': seasonal_df,
            'measure': measure_df,
            'border': border_df,
            'ports': ports_df
        }
        
    except Exception as e:
        logger.error(f"Error in data aggregation pipeline: {str(e)}")
        raise


def main():
    """
    Main function that orchestrates the data aggregation pipeline.
    
    This function serves as the entry point when the script is run directly.
    It calls the aggregate_data function and provides summary statistics.
    """
    try:
        # Run the aggregation pipeline
        aggregated_datasets = aggregate_data()
        
        print(f"\n" + "="*60)
        print("DATA AGGREGATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        # Print summary statistics for each dataset
        print(f"\n📊 AGGREGATED DATASETS SUMMARY:")
        print(f"{'Dataset':<30} {'Records':<10} {'Description'}")
        print(f"{'-'*30} {'-'*10} {'-'*40}")
        
        dataset_info = [
            ('Monthly Crossings', 'monthly', 'Total monthly trends over time'),
            ('Seasonal Crossings', 'seasonal', 'Average crossings by season'),
            ('Measure Crossings', 'measure', 'Monthly data by transportation type'),
            ('Border Region Crossings', 'border', 'Monthly data by border region'),
            ('Top Ports (2000s)', 'ports', 'Busiest ports since 2000')
        ]
        
        for name, key, description in dataset_info:
            if key in aggregated_datasets and not aggregated_datasets[key].empty:
                count = len(aggregated_datasets[key])
                print(f"{name:<30} {count:<10} {description}")
            else:
                print(f"{name:<30} {'0':<10} {description} (EMPTY)")
        
        print(f"\n✅ All aggregated files saved to: data/processed/")
        print(f"📁 Files created:")
        files = [
            'monthly_crossings.csv',
            'seasonal_crossings.csv', 
            'measure_crossings.csv',
            'border_region_crossings.csv',
            'top_ports_crossings_2000s.csv'
        ]
        
        for file in files:
            print(f"   • {file}")
        
        print(f"\n🎯 Ready for analysis notebooks!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())