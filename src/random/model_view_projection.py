from pyglm import glm


class MVP:
    # Model
    model_matrix = glm.mat4(1.0)
    model_scale_x, model_scale_y, model_scale_z = 0.4, -0.3, 0.8
    model_matrix = glm.scale(model_matrix, glm.vec3(model_scale_x, model_scale_y, model_scale_z))
    # View
    camera_start_pos = glm.vec3(0.0, -5.0, 5.0)  # Camera at (0,0,15)
    look_at = glm.vec3(0.0, 0.0, 0.0)  # Looking at the origin
    up_vector = glm.vec3(0.0, 1.0, 0.0)  # Y-axis is up
    unscrolled_view_matrix = glm.lookAt(camera_start_pos, look_at, up_vector)
    # Perspective
    fovy_deg = 45.0
    screen_width, screen_height = 1600, 900
    aspect_ratio = screen_width / screen_height
    near_plane, far_plane = 1.0, 100.0
    projection_matrix = glm.perspective(glm.radians(fovy_deg), aspect_ratio, near_plane, far_plane)

    def __init__(self, scroll):
        self.scroll = scroll
        self.view_matrix = glm.lookAt(self.camera_start_pos, self.look_at, self.up_vector)
        self.mvp_matrix = self.projection_matrix * self.view_matrix * self.model_matrix

    def update_view_matrix(self):
        scrolled_camera_pos = self.camera_start_pos + glm.vec3(self.scroll.x / 200, -self.scroll.y / 200, -self.scroll.z)
        scrolled_look_at = self.look_at + glm.vec3(self.scroll.x / 200, -self.scroll.y / 200, 0)
        self.view_matrix =  glm.lookAt(scrolled_camera_pos, scrolled_look_at, self.up_vector)

    def update_mvp_matrix(self):
        self.mvp_matrix = self.projection_matrix * self.view_matrix * self.model_matrix

    def update(self):
        scrolled_camera_pos = self.camera_start_pos + glm.vec3(self.scroll.x / 200, -self.scroll.y / 200, -self.scroll.z)
        scrolled_look_at = self.look_at + glm.vec3(self.scroll.x / 200, -self.scroll.y / 200, 0)
        self.view_matrix =  glm.lookAt(scrolled_camera_pos, scrolled_look_at, self.up_vector)
        self.mvp_matrix = self.projection_matrix * self.view_matrix * self.model_matrix
        return self.mvp_matrix




