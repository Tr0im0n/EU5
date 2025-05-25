import numpy as np
import csv

# Re-create the TileColors class with normalized RGB values (0.0-1.0)
# This is necessary to map the tile_type strings from the CSV to actual colors.
class TileColors:
    GRASSLAND = (0.486, 0.733, 0.333, 1.0)
    FARMLAND  = (0.745, 0.706, 0.431, 1.0)
    WOODS     = (0.314, 0.510, 0.314, 1.0)
    FOREST    = (0.157, 0.392, 0.157, 1.0)
    HILL      = (0.588, 0.471, 0.314, 1.0)
    MOUNTAIN  = (0.471, 0.490, 0.510, 1.0)
    COASTAL_WATER = (0.510, 0.784, 0.902, 1.0)
    OCEAN         = (0.235, 0.471, 0.706, 1.0)

    @classmethod
    def get_color(cls, tile_type: str) -> tuple[float, float, float, float] | None:
        return getattr(cls, tile_type.upper(), None)

# Define the CSV file name
csv_file_name = "korea.csv"

# --- Step 1: Determine the grid dimensions ---
# We need to do a first pass to figure out max q and r
max_q = 0
max_r = 0
try:
    with open(csv_file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            q = int(row['q'])
            r = int(row['r'])
            if q > max_q:
                max_q = q
            if r > max_r:
                max_r = r
except FileNotFoundError:
    print(f"Error: The file '{csv_file_name}' was not found. Please make sure it exists.")
    exit()
except KeyError as e:
    print(f"Error: Missing column in CSV. Make sure 'q', 'r', and 'tile_type' columns exist. Missing: {e}")
    exit()

grid_width = max_q + 1
grid_height = max_r + 1
total_tiles = grid_width * grid_height

print(f"Detected grid dimensions: {grid_width}x{grid_height} (Total tiles: {total_tiles})")

# --- Step 2: Initialize the NumPy array ---
# Shape will be (total_tiles, 3) for RGB (3 color channels)
tile_colors_array = np.zeros((total_tiles, 3), dtype=np.float32)

# --- Step 3: Read the CSV data and populate the array ---
try:
    with open(csv_file_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            q = int(row['q'])
            r = int(row['r'])
            tile_type_str = row['tile_type']

            # Calculate the linear index for the tile in a row-major order
            linear_index = r * grid_width + q

            # Get the RGBA color from TileColors and take only the RGB part
            color_rgba = TileColors.get_color(tile_type_str)
            if color_rgba:
                tile_colors_array[linear_index] = color_rgba[:3] # Take R, G, B
            else:
                # Handle unknown tile types by assigning a default color (e.g., black)
                print(f"Warning: Unknown tile type '{tile_type_str}' at ({q},{r}). Assigning black.")
                tile_colors_array[linear_index] = (0.0, 0.0, 0.0) # Black for unknown types

except FileNotFoundError:
    # This error should ideally be caught by the first try-except block, but good to have
    print(f"Fatal Error: The file '{csv_file_name}' was not found during data reading.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while processing the CSV: {e}")
    exit()

print("\nSuccessfully created tile_colors_array:")
print(f"Shape: {tile_colors_array.shape}")
print(f"Data type: {tile_colors_array.dtype}")

# --- Example Usage (Optional) ---
# Print the color of a specific tile
print(f"\nColor of tile (0, 0): {tile_colors_array[0 * grid_width + 0]}") # Expected: MOUNTAIN color
print(f"Color of tile (5, 3): {tile_colors_array[3 * grid_width + 5]}") # Expected: COASTAL_WATER color
print(f"Color of tile (4, 4): {tile_colors_array[4 * grid_width + 4]}") # Expected: OCEAN color