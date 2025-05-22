from src.hex_grid.hex_grid import get_hex_grid_center_cords_old, get_hex_grid_center_cords, get_all_hex_line_cords, \
    add_perspective_along_axis, add_perspective_vectorized, get_all_hex_line_cords_stack
from utils.timing import compare_function_speed


def hex_grid_center():
    width, height = 1000, 1000  # Example arguments
    compare_function_speed(
        get_hex_grid_center_cords_old,
        get_hex_grid_center_cords,
        args=(width, height),
        func1_name="Loop-based",
        func2_name="Vectorized"
    )


def lines():
    width, height = 10, 10
    center_cords = get_hex_grid_center_cords(width, height)
    # a = get_all_hex_line_cords(center_cords)
    # b = get_all_hex_line_cords_stack(center_cords)
    # print(a==b)
    compare_function_speed(
        get_all_hex_line_cords,
        get_all_hex_line_cords_stack,
        args=(center_cords,),
        func1_name="Along Axis",
        func2_name="Vectorized"
    )


def perspective():
    width, height = 100, 100
    center_cords = get_hex_grid_center_cords(width, height)
    lines_points = get_all_hex_line_cords(center_cords)
    print("Completed initializing")
    compare_function_speed(
        add_perspective_along_axis,
        add_perspective_vectorized,
        args=(lines_points, ),
        func1_name="Along Axis",
        func2_name="Vectorized"
    )


if __name__ == "__main__":
    # hex_grid_center()
    lines()
    # perspective()










