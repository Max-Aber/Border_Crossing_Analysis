"""
Utility functions for plotting data quicker.
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_graph(x, y, title, xlabel, ylabel):
    """
    Plots a graph with the given x and y data.

    Parameters:
    - x: The x-axis data.
    - y: The y-axis data.
    - title: The title of the graph.
    - xlabel: The label for the x-axis.
    - ylabel: The label for the y-axis.
    """
    
    plt.figure(figsize=(25, 5))
    plt.plot(x, y)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    
    plt.grid(True)
    
    plt.show()

def plot_border_transportation(df, border_name, transportation_type=None):
    """
    Plot border crossings for a specific border and transportation type.
    
    Parameters:
    - df: The cleaned border crossing dataframe
    - border_name: 'Canada' or 'Mexico'
    - transportation_type: Specific type or None for all types
    """
    
    # Filter by border
    border_data = df[df['Border'] == border_name].copy()
    
    if transportation_type:
        # Plot specific transportation type
        transport_data = border_data[border_data['Measure'] == transportation_type]
        
        plt.figure(figsize=(15, 6))
        plt.plot(transport_data['Date'], transport_data['Value'], marker='o')
        plt.title(f'{border_name} Border - {transportation_type} Crossings Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Crossings')
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
    else:
        # Plot all transportation types for the border
        plt.figure(figsize=(15, 8))
        
        transportation_types = border_data['Measure'].unique()
        
        for transport_type in transportation_types:
            type_data = border_data[border_data['Measure'] == transport_type]
            plt.plot(type_data['Date'], type_data['Value'], 
                    marker='o', label=transport_type, linewidth=2)
        
        plt.title(f'{border_name} Border - All Transportation Types Over Time')
        plt.xlabel('Date')
        plt.ylabel('Number of Crossings')
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

def plot_transportation_comparison(df, transportation_type):
    """
    Compare a specific transportation type between Canada and Mexico borders.
    
    Parameters:
    - df: The cleaned border crossing dataframe
    - transportation_type: Type of transportation to compare
    """
    
    # Filter by transportation type
    transport_data = df[df['Measure'] == transportation_type].copy()
    
    plt.figure(figsize=(15, 6))
    
    # Plot Canada and Mexico separately
    for border in ['Canada', 'Mexico']:
        border_data = transport_data[transport_data['Border'] == border]
        plt.plot(border_data['Date'], border_data['Value'], 
                marker='o', label=f'{border} Border', linewidth=2)
    
    plt.title(f'{transportation_type} - Canada vs Mexico Border Comparison')
    plt.xlabel('Date')
    plt.ylabel('Number of Crossings')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_total_border_crossings(df):
    """
    Plot total crossings for each border (all transportation types combined).
    
    Parameters:
    - df: The cleaned border crossing dataframe
    """
    
    # Group by date and border, sum all transportation types
    total_by_border = df.groupby(['Date', 'Border'])['Value'].sum().reset_index()
    
    plt.figure(figsize=(15, 6))
    
    for border in ['Canada', 'Mexico']:
        border_data = total_by_border[total_by_border['Border'] == border]
        plt.plot(border_data['Date'], border_data['Value'], 
                marker='o', label=f'{border} Border', linewidth=3)
    
    plt.title('Total Border Crossings - Canada vs Mexico')
    plt.xlabel('Date')
    plt.ylabel('Total Crossings (All Transportation)')
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    plt.show()