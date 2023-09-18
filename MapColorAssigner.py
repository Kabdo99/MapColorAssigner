"""
@author: Abdullah Alkhamis with assistance of ChatGPT
@class: CSCV 471: Artificial Intelligence, Fall 23'
@instructor: Dr. Karen Hand
@goals: • Understand the search techniques to solve real-world problems
        • Analyze the blind-search technique
        • Analyze the heuristic search
        • Analyze the greedy-search algorithm
        • Analyze the adversarial search
        • Use the help of AI tools to analyze their behavior
@description: A program to solve the USA map coloring problem using the Four-Color Theorem. 
              Utilizes backtracking to ensure no two adjacent states share the same color 
              and visualizes the solution using GeoPandas and Matplotlib.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def visualize_map_coloring(coloring):
    """
    This function visualizes the coloring of the US map based on a given coloring solution.

    Parameters:
        - coloring (dict): A dictionary where keys are state names and values are the assigned colors.
    
    The function uses GeoPandas to load the US map and maps each state to its respective color
    from the provided coloring solution. It then uses Matplotlib to visualize the colored map.
    """
    # Load US states from a direct GeoJSON link
    url = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json"
    states_df = gpd.read_file(url)
    
    # Convert state names to the common ones used in your adjacency list
    states_df['name'] = states_df['NAME']
    
    # Map the colors from your coloring algorithm to the 'color' column in the GeoDataFrame
    states_df['color'] = states_df['name'].map(coloring)
    
    # Convert colors to RGB
    color_dict = {
        "Red": "red",
        "Yellow": "yellow",
        "Blue": "blue",
        "Green": "green"
    }
    states_df['facecolor'] = states_df['color'].map(color_dict)
    
    # Plot
    fig, ax = plt.subplots(figsize=(15,10))
    states_df.boundary.plot(ax=ax, linewidth=1)
    
    for idx, row in states_df.iterrows():
        if pd.isna(row['facecolor']):
            print(f"Warning: Missing color for {row['name']}")  # print a warning message
            continue  # skip the state

        if row['geometry'].geom_type == 'Polygon':
            ax.fill(*row['geometry'].exterior.xy, facecolor=row['facecolor'])
        else:  # it's a MultiPolygon
            for polygon in row['geometry'].geoms:
                ax.fill(*polygon.exterior.xy, facecolor=row['facecolor'])
    plt.title("USA Map Coloring")
    plt.show()

def is_valid_coloring(state, color, current_coloring, adjacency_list):
    """
    Checks if it's valid to color the given state with the given color.
    
    Parameters:
        - state (str): The name of the state to check.
        - color (str): The color to validate for the state.
        - current_coloring (dict): A dictionary representing the current state color assignments.
        - adjacency_list (dict): A dictionary representing the adjacency relations between states.
    
    Returns:
        - bool: True if it's valid to color the state with the color, False otherwise.
        
    The function checks if any neighboring state of the given state already has the same color.
    """
    for neighbor in adjacency_list[state]:
        if current_coloring.get(neighbor) == color:
            return False
    return True

def backtrack_coloring(current_coloring, states, adjacency_list):
    """
    Uses backtracking to find a valid coloring for the US map.
    
    Parameters:
        - current_coloring (dict): A dictionary representing the current state color assignments.
        - states (list): A list of states left to color.
        - adjacency_list (dict): A dictionary representing the adjacency relations between states.
    
    Returns:
        - dict: A valid coloring if one exists, None otherwise.
        
    The function tries to assign one of the four colors to each state, recursively attempting
    to color the remaining states. If no valid coloring is found for a state, it backtracks and
    tries another color for the previous state.
    """
    if not states:  # If all states are colored, we found a solution
        return current_coloring

    current_state = states[0]
    colors = ["Red", "Yellow", "Blue", "Green"]

    for color in colors:
        if is_valid_coloring(current_state, color, current_coloring, adjacency_list):
            new_coloring = current_coloring.copy()
            new_coloring[current_state] = color

            # Recursively color the rest of the states
            result = backtrack_coloring(new_coloring, states[1:], adjacency_list)

            if result:
                return result
    return None  # This path leads to no valid coloring, so backtrack

def main():
    # Create an adjacency list where states are keys and lists of neighboring states are values
    adjacency_list = {
    'Alabama': ['Florida', 'Georgia', 'Mississippi', 'Tennessee'],
    'Alaska': [],  # Excluding non-contiguous states
    'Arizona': ['California', 'Colorado', 'Nevada', 'New Mexico', 'Utah'],
    'Arkansas': ['Louisiana', 'Mississippi', 'Missouri', 'Oklahoma', 'Tennessee', 'Texas'],
    'California': ['Arizona', 'Nevada', 'Oregon'],
    'Colorado': ['Arizona', 'Kansas', 'Nebraska', 'New Mexico', 'Oklahoma', 'Utah', 'Wyoming'],
    'Connecticut': ['Massachusetts', 'New York', 'Rhode Island'],
    'Delaware': ['Maryland', 'New Jersey', 'Pennsylvania'],
    'Florida': ['Alabama', 'Georgia'],
    'Georgia': ['Alabama', 'Florida', 'North Carolina', 'South Carolina', 'Tennessee'],
    'Hawaii': [],  # Excluding non-contiguous states
    'Idaho': ['Montana', 'Nevada', 'Oregon', 'Utah', 'Washington', 'Wyoming'],
    'Illinois': ['Indiana', 'Iowa', 'Kentucky', 'Missouri', 'Wisconsin'],
    'Indiana': ['Illinois', 'Kentucky', 'Michigan', 'Ohio'],
    'Iowa': ['Illinois', 'Minnesota', 'Missouri', 'Nebraska', 'South Dakota', 'Wisconsin'],
    'Kansas': ['Colorado', 'Missouri', 'Nebraska', 'Oklahoma'],
    'Kentucky': ['Illinois', 'Indiana', 'Missouri', 'Ohio', 'Tennessee', 'Virginia', 'West Virginia'],
    'Louisiana': ['Arkansas', 'Mississippi', 'Texas'],
    'Maine': ['New Hampshire'],
    'Maryland': ['Delaware', 'Pennsylvania', 'Virginia', 'West Virginia'],
    'Massachusetts': ['Connecticut', 'New Hampshire', 'New York', 'Rhode Island', 'Vermont'],
    'Michigan': ['Indiana', 'Ohio', 'Wisconsin'],
    'Minnesota': ['Iowa', 'North Dakota', 'South Dakota', 'Wisconsin'],
    'Mississippi': ['Alabama', 'Arkansas', 'Louisiana', 'Tennessee'],
    'Missouri': ['Arkansas', 'Illinois', 'Iowa', 'Kansas', 'Kentucky', 'Nebraska', 'Oklahoma', 'Tennessee'],
    'Montana': ['Idaho', 'North Dakota', 'South Dakota', 'Wyoming'],
    'Nebraska': ['Colorado', 'Iowa', 'Kansas', 'Missouri', 'South Dakota', 'Wyoming'],
    'Nevada': ['Arizona', 'California', 'Idaho', 'Oregon', 'Utah'],
    'New Hampshire': ['Maine', 'Massachusetts', 'Vermont'],
    'New Jersey': ['Delaware', 'New York', 'Pennsylvania'],
    'New Mexico': ['Arizona', 'Colorado', 'Oklahoma', 'Texas', 'Utah'],
    'New York': ['Connecticut', 'Massachusetts', 'New Jersey', 'Pennsylvania', 'Rhode Island', 'Vermont'],
    'North Carolina': ['Georgia', 'South Carolina', 'Tennessee', 'Virginia'],
    'North Dakota': ['Minnesota', 'Montana', 'South Dakota'],
    'Ohio': ['Indiana', 'Kentucky', 'Michigan', 'Pennsylvania', 'West Virginia'],
    'Oklahoma': ['Arkansas', 'Colorado', 'Kansas', 'Missouri', 'New Mexico', 'Texas'],
    'Oregon': ['California', 'Idaho', 'Nevada', 'Washington'],
    'Pennsylvania': ['Delaware', 'Maryland', 'New Jersey', 'New York', 'Ohio', 'West Virginia'],
    'Rhode Island': ['Connecticut', 'Massachusetts', 'New York'],
    'South Carolina': ['Georgia', 'North Carolina'],
    'South Dakota': ['Iowa', 'Minnesota', 'Montana', 'Nebraska', 'North Dakota', 'Wyoming'],
    'Tennessee': ['Alabama', 'Arkansas', 'Georgia', 'Kentucky', 'Mississippi', 'Missouri', 'North Carolina', 'Virginia'],
    'Texas': ['Arkansas', 'Louisiana', 'New Mexico', 'Oklahoma'],
    'Utah': ['Arizona', 'Colorado', 'Idaho', 'Nevada', 'New Mexico', 'Wyoming'],
    'Vermont': ['Massachusetts', 'New Hampshire', 'New York'],
    'Virginia': ['Kentucky', 'Maryland', 'North Carolina', 'Tennessee', 'West Virginia'],
    'Washington': ['Idaho', 'Oregon'],
    'West Virginia': ['Kentucky', 'Maryland', 'Ohio', 'Pennsylvania', 'Virginia'],
    'Wisconsin': ['Illinois', 'Iowa', 'Michigan', 'Minnesota'],
    'Wyoming': ['Colorado', 'Idaho', 'Montana', 'Nebraska', 'South Dakota', 'Utah']
    }

    states = list(adjacency_list.keys())
    coloring = backtrack_coloring({}, states, adjacency_list)
    print(coloring)
    visualize_map_coloring(coloring)

if __name__ == "__main__":
    main()