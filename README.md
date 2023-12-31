# MapColorAssigner

This Python program is designed to color the U.S. map, ensuring no adjacent states have the same color. It utilizes only four colors to achieve this. The program first starts with a blank map and goes state by state, assigning colors while making sure neighboring states aren't using that same color. If the script finds itself stuck, it backtracks to try different color combinations. Once every state is colored, the script displays a visual representation of the U.S. map with our color choices, ensuring that no neighboring states share the same hue. It's a digital take on a classic puzzle, where the goal is to find the right mix of colors for the entire country.

# Tools Used:
2. GeoPandas: A Python library utilized for geographical data manipulation, which made it possible to handle and visualize the U.S. map data.
3. Matplotlib: A plotting library for Python, used in conjunction with GeoPandas to visually display the colored U.S. map.
4. ChatGPT
