import csv

# Define the grid size
GRID_WIDTH = 20
GRID_HEIGHT = 20


def start():
    # Create a dictionary to hold our hex map data
    high_res_hex_map = {}

    # --- Logic to assign tile types based on (q, r) coordinates ---
    # This is a manual approximation of the geography
    # q increases to the right (east), r increases downwards (south)

    for r in range(GRID_HEIGHT):
        for q in range(GRID_WIDTH):
            tile_type = "OCEAN"  # Default to ocean

            # --- Manchuria Region (Northern rows) ---
            if r <= 5:  # Rows 0-5: Primarily Manchuria
                if q <= 3:  # Far West: Mountains (Greater Khingan / part of Siberia border)
                    tile_type = "MOUNTAIN"
                elif q <= 7:  # West-Central: Forests (Taiga-like)
                    tile_type = "FOREST"
                elif q <= 13:  # Central: Grasslands & Farmland (Songliao Plain)
                    if r < 3 and q > 9:
                        tile_type = "GRASSLAND"  # North Grasslands
                    else:
                        tile_type = "FARMLAND"  # More arable further south
                elif q <= 16:  # East: Forests (Eastern Manchurian forests)
                    tile_type = "FOREST"
                else:  # Far East: More mountains/forests bordering Russia/North Korea
                    tile_type = "MOUNTAIN"

            # --- Transition: Southern Manchuria / Northern Korea / Inner Mongolia / North China ---
            elif r <= 10:  # Rows 6-10
                if q <= 1:  # West edge: Hills/Grassland (Inner Mongolia transition)
                    tile_type = "HILL"
                elif q <= 5:  # NW China / Southern Manchuria: Farmland / Grassland
                    tile_type = "FARMLAND" if r > 7 else "GRASSLAND"
                elif q <= 9:  # North China Plain / Bohai Gulf area start
                    if r <= 7:
                        tile_type = "FARMLAND"  # More farmland
                    elif r == 8 and q >= 6:
                        tile_type = "COASTAL_WATER"  # Start of Bohai Gulf
                    elif r == 9 and q >= 5:
                        tile_type = "COASTAL_WATER"
                    elif r == 10 and q >= 4:
                        tile_type = "COASTAL_WATER"
                    else:
                        tile_type = "FARMLAND"  # North China plain
                elif q <= 14:  # North Korea (Korean Peninsula base)
                    if q >= 10 and q <= 11:
                        tile_type = "MOUNTAIN"  # Mountain spine
                    else:
                        tile_type = "HILL"
                    if r > 8 and q > 12: tile_type = "GRASSLAND"  # Near coast
                else:  # East of Korea / Sea of Japan
                    if r > 8 and q <= 15:
                        tile_type = "COASTAL_WATER"
                    else:
                        tile_type = "OCEAN"

            # --- Korea Peninsula / Northern Coastal China / Yellow Sea ---
            elif r <= 15:  # Rows 11-15
                if q <= 2:  # Northern China Coast / Shandong Peninsula (west side)
                    if r == 11 and q <= 1:
                        tile_type = "FARMLAND"
                    elif r == 12 and q == 0:
                        tile_type = "FARMLAND"
                    else:
                        tile_type = "COASTAL_WATER"
                elif q <= 6:  # Yellow Sea (west side)
                    tile_type = "OCEAN"
                elif q <= 11:  # Korean Peninsula (main body)
                    if q == 7 or q == 8:
                        tile_type = "MOUNTAIN"  # Central mountain range
                    elif q == 9 or q == 10:
                        tile_type = "HILL"
                    else:
                        tile_type = "FARMLAND" if r < 14 else "GRASSLAND"  # Coastal plains
                elif q <= 14:  # East of Korea / Sea of Japan
                    tile_type = "COASTAL_WATER"
                else:  # Sea of Japan (deeper)
                    tile_type = "OCEAN"

            # --- Southern Korea / Yellow Sea / East China Sea ---
            else:  # r >= 16
                if q <= 2:  # Southern China Coast / East China Sea
                    if r == 16 and q == 0:
                        tile_type = "FARMLAND"
                    elif r == 17 and q == 0:
                        tile_type = "FARMLAND"
                    else:
                        tile_type = "OCEAN"
                elif q <= 6:  # Yellow Sea / East China Sea
                    tile_type = "OCEAN"
                elif q <= 10:  # Southern Korean tip / Islands
                    if r == 16 and q >= 7:
                        tile_type = "COASTAL_WATER"  # South coast
                    elif r == 17 and q >= 7:
                        tile_type = "COASTAL_WATER"
                    elif r == 18 and q == 8:
                        tile_type = "COASTAL_WATER"  # Islands
                    else:
                        tile_type = "OCEAN"
                else:  # Open Ocean
                    tile_type = "OCEAN"

            # Override for specific notable features or general smoothing
            if r == 13 and q == 1: tile_type = "FARMLAND"  # Small land patch in China
            if r == 16 and q == 6: tile_type = "OCEAN"  # Ensure no stray land
            if r == 17 and q == 6: tile_type = "OCEAN"

            high_res_hex_map[(q, r)] = tile_type

    # Define the output file name
    output_file_name = "../../assets/hex_grid/korea_manchuria_hires.csv"

    # Write the map data to the CSV file
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['q', 'r', 'tile_type'])  # Write the header row
        for r in range(GRID_HEIGHT):
            for q in range(GRID_WIDTH):
                writer.writerow([q, r, high_res_hex_map[(q, r)]])

    print(f"Generated a {GRID_WIDTH}x{GRID_HEIGHT} hex map CSV: '{output_file_name}'")
    print(f"Total tiles: {GRID_WIDTH * GRID_HEIGHT}")