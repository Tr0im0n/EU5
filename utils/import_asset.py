import os
from PIL import Image


def import_shader(file_name):

    current_script_path = os.path.abspath(__file__)
    root_directory = os.path.join(current_script_path, "..", "..")

    with open(os.path.join(root_directory, 'assets', 'shaders', file_name), 'r') as file:
        ans = file.read()
    return ans


def import_texture(file_name):

    current_script_path = os.path.abspath(__file__)
    root_directory = os.path.join(current_script_path, "..", "..")

    return Image.open(os.path.join(root_directory, 'assets', 'textures', file_name)).convert('RGBA')


