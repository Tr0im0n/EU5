from src.hex_grid.hex_grid import get_hex_grid_center_cords_old, get_hex_grid_center_cords
from utils.timing import compare_function_speed

if __name__ == "__main__":
    width, height = 100, 100  # Example arguments
    compare_function_speed(
        get_hex_grid_center_cords_old,
        get_hex_grid_center_cords,
        args=(width, height),
        func1_name="Loop-based",
        func2_name="Vectorized"
    )










