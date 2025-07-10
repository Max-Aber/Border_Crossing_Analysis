import matplotlib.pyplot as plt

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
    
    plt.figure(figsize=(25, 15))
    plt.plot(x, y)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.grid(True)
    
    plt.show()