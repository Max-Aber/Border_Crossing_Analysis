"""
Comprehensive plotting utilities for border crossing data analysis.
Contains both general-purpose plotting functions and domain-specific visualizations.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter
import numpy as np

# Set professional styling
plt.style.use('default')
sns.set_palette("husl")

# ============================================================================
# GENERAL PLOTTING UTILITIES (Reusable across any project)
# ============================================================================

def plot_time_series(df, x_col, y_col, title=None, xlabel=None, ylabel=None, 
                    figsize=(12, 6), color=None, marker='o'):
    """
    Create a basic time series plot.
    
    Args:
        df: DataFrame containing the data
        x_col: Column name for x-axis (usually dates)
        y_col: Column name for y-axis (values)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size tuple
        color: Line color
        marker: Marker style
    """
    plt.figure(figsize=figsize)
    plt.plot(df[x_col], df[y_col], marker=marker, linestyle='-', color=color)
    plt.title(title or f'Time Series of {y_col}')
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or y_col)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_multiple_lines(df, x_col, y_cols, title=None, xlabel=None, ylabel=None, 
                       figsize=(14, 8), legend_labels=None):
    """
    Plot multiple lines on the same chart for comparison.
    
    Args:
        df: DataFrame containing the data
        x_col: Column name for x-axis
        y_cols: List of column names for y-axis
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size tuple
        legend_labels: Custom legend labels
    """
    plt.figure(figsize=figsize)
    
    for i, col in enumerate(y_cols):
        label = legend_labels[i] if legend_labels else col
        plt.plot(df[x_col], df[col], marker='o', label=label, linewidth=2)
    
    plt.title(title or 'Multi-Line Comparison')
    plt.xlabel(xlabel or x_col)
    plt.ylabel(ylabel or 'Values')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_bar_chart(df, x_col, y_col, title=None, xlabel=None, ylabel=None, 
                  figsize=(12, 6), color='skyblue', horizontal=False):
    """
    Create a bar chart.
    
    Args:
        df: DataFrame containing the data
        x_col: Column name for x-axis (categories)
        y_col: Column name for y-axis (values)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure size tuple
        color: Bar color
        horizontal: If True, create horizontal bar chart
    """
    plt.figure(figsize=figsize)
    
    if horizontal:
        plt.barh(df[x_col], df[y_col], color=color)
        plt.xlabel(ylabel or y_col)
        plt.ylabel(xlabel or x_col)
    else:
        plt.bar(df[x_col], df[y_col], color=color)
        plt.xlabel(xlabel or x_col)
        plt.ylabel(ylabel or y_col)
        plt.xticks(rotation=45)
    
    plt.title(title or f'{y_col} by {x_col}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# ============================================================================
# DOMAIN-SPECIFIC FUNCTIONS (Border crossing specific)
# ============================================================================

def plot_border_comparison(monthly_df, title="Canada vs Mexico Border Crossings Over Time"):
    """
    Compare total crossings between Canada and Mexico borders over time.
    
    Args:
        monthly_df: DataFrame with Date and border-specific columns or grouped data
        title: Plot title
    """
    plt.figure(figsize=(15, 8))
    
    # If data has 'Border' column, pivot it
    if 'Border' in monthly_df.columns:
        pivot_df = monthly_df.pivot_table(
            index='Date', 
            columns='Border', 
            values='Monthly_Crossings', 
            fill_value=0
        )
        
        for border in pivot_df.columns:
            plt.plot(pivot_df.index, pivot_df[border], 
                    marker='o', linewidth=2, label=border)
    else:
        # Assume columns are already separated
        for col in monthly_df.columns:
            if col != 'Date':
                plt.plot(monthly_df['Date'], monthly_df[col], 
                        marker='o', linewidth=2, label=col)
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Monthly Crossings (Millions)', fontsize=12)
    
    # Format y-axis to show millions
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_transportation_trends(measure_df, title="Transportation Type Trends Over Time"):
    """
    Plot trends for different transportation types.
    
    Args:
        measure_df: DataFrame with Date, transportation measures
        title: Plot title
    """
    plt.figure(figsize=(16, 10))
    
    # If data has 'Measure' column, pivot it
    if 'Measure' in measure_df.columns:
        pivot_df = measure_df.pivot_table(
            index='Date', 
            columns='Measure', 
            values='Monthly_Crossings', 
            fill_value=0
        )
        transportation_types = pivot_df.columns
        plot_data = pivot_df
    else:
        # Assume columns are already separated
        transportation_types = [col for col in measure_df.columns if col != 'Date']
        plot_data = measure_df.set_index('Date')
    
    # Create subplots for each transportation type
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, transport_type in enumerate(transportation_types[:4]):  # Limit to 4
        ax = axes[i]
        ax.plot(plot_data.index, plot_data[transport_type], 
               color=colors[i], linewidth=2, marker='o', markersize=4)
        ax.set_title(f'{transport_type}', fontsize=12, fontweight='bold')
        ax.set_ylabel('Monthly Crossings')
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
        
        # Format y-axis
        if plot_data[transport_type].max() > 1e6:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        elif plot_data[transport_type].max() > 1e3:
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_seasonal_patterns(seasonal_df, title="Average Border Crossings by Season"):
    """
    Create a seasonal pattern visualization.
    
    Args:
        seasonal_df: DataFrame with seasons and crossing data
        title: Plot title
    """
    plt.figure(figsize=(12, 8))
    
    # Ensure proper season order
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    if 'Season' in seasonal_df.columns:
        plot_df = seasonal_df.set_index('Season').reindex(season_order)
        values = plot_df['Avg_Monthly_Crossings']
        std_values = plot_df.get('Std_Monthly_Crossings', None)
    else:
        values = seasonal_df['Avg_Monthly_Crossings']
        std_values = seasonal_df.get('Std_Monthly_Crossings', None)
    
    bars = plt.bar(season_order, values, 
                   color=['lightblue', 'lightgreen', 'orange', 'brown'],
                   alpha=0.7, edgecolor='black', linewidth=1)
    
    # Add error bars if standard deviation is available
    if std_values is not None:
        plt.errorbar(season_order, values, yerr=std_values, 
                    fmt='none', color='black', capsize=5)
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Average Monthly Crossings (Millions)', fontsize=12)
    
    # Format y-axis
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + value*0.01,
                f'{value/1e6:.1f}M', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

def plot_top_ports(ports_df, top_n=10, title=None):
    """
    Create a horizontal bar chart of top ports by crossing volume.
    
    Args:
        ports_df: DataFrame with port data
        top_n: Number of top ports to show
        title: Plot title
    """
    # Get top N ports
    top_ports = ports_df.nlargest(top_n, 'Total_Crossings')
    
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar chart
    bars = plt.barh(range(len(top_ports)), top_ports['Total_Crossings'], 
                    color='steelblue', alpha=0.7)
    
    plt.yticks(range(len(top_ports)), 
               [f"{row['Port Name']}, {row['State']}" for _, row in top_ports.iterrows()])
    
    plt.xlabel('Total Crossings (Millions)', fontsize=12)
    plt.ylabel('Port', fontsize=12)
    plt.title(title or f'Top {top_n} Busiest Border Ports (Since 2000)', 
              fontsize=14, fontweight='bold')
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_ports['Total_Crossings'])):
        plt.text(value + value*0.01, bar.get_y() + bar.get_height()/2,
                f'{value/1e6:.1f}M', va='center', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.show()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_millions(ax, axis='y'):
    """Format axis to show values in millions."""
    if axis == 'y':
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    else:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

def format_thousands(ax, axis='y'):
    """Format axis to show values in thousands."""
    if axis == 'y':
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))
    else:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e3:.0f}K'))

def set_professional_style():
    """Set professional plotting style for all charts."""
    plt.rcParams.update({
        'figure.figsize': (12, 8),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11,
        'grid.alpha': 0.3
    })