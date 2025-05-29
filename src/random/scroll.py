

class Scroll:
    def __init__(self, x_lb=-2000.0, x_ub=20000.0, y_lb=-2000.0, y_ub=20000.0, z_lb=-4.0, z_ub=4.0):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.x_lb = x_lb
        self.x_ub = x_ub
        self.y_lb = y_lb
        self.y_ub = y_ub
        self.z_lb = z_lb
        self.z_ub = z_ub

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = max(self.x_lb, min(self.x_ub, value))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = max(self.y_lb, min(self.y_ub, value))

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = max(self.z_lb, min(self.z_ub, value))

    def __str__(self):
        return f"x = {self._x}, y = {self._y}, z = {self._z}"