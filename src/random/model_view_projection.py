from pyglm import glm


class MVP:
    camera_pos = glm.vec3(0.0, -3.0, 5.0)  # Camera at (0,0,15)
    look_at = glm.vec3(0.0, 0.0, 0.0)  # Looking at the origin
    up_vector = glm.vec3(0.0, 1.0, 0.0)  # Y-axis is up
    view_matrix = glm.lookAt(camera_pos, look_at, up_vector)

    fovy_deg = 45.0
    screen_width, screen_height = 1600, 900
    aspect_ratio = screen_width / screen_height
    near_plane, far_plane = 1.0, 100.0
    projection_matrix = glm.perspective(glm.radians(fovy_deg), aspect_ratio, near_plane, far_plane)

    model_matrix = glm.mat4(1.0)
    model_scale = 0.1  # Adjust this based on your HexGrid's coordinate range
    model_matrix = glm.scale(model_matrix, glm.vec3(model_scale, -model_scale, model_scale))
    # model_matrix = glm.translate(model_matrix, glm.vec3(-8.0, -4.5, 0.0))  # Center 16x9 grid











