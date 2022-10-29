import numpy as np
import math
from modules.displays import Display
from modules.size_interpolation import Interpolate

class Rotation:
    t_array = []

    def __init__(self, array):
        self.t_array = array

    def construct_t(self):
        Rotation.t_array = np.zeros( (128,128), dtype=np.uint8)
        Rotation.t_array[28:49,28:99] = 255
        Rotation.t_array[48:99,53:74] = 255

        Display.display_image(self, self.rotation_figure, Rotation.t_array)

    def rotate(self, angle, type):

        # Convert imput angle to rad
        rad = math.radians(angle)

        # Create new array for rotated image
        rotated_array = np.zeros( (Rotation.t_array.shape), dtype=np.uint8)

        # Rotated array width and height
        width = rotated_array.shape[0]
        height = rotated_array.shape[1]

        # Center of rotation
        mid_x = width // 2
        mid_y = height // 2

        for i in range(height):
            for j in range(width):

                # Find rotated coordinates of each pixel
                # Subtracting mid_x and mid_y to translate it the origin before rotating ----> (T^-1)RT
                x = math.cos(rad) * (i - mid_x) + math.sin(rad) * (j - mid_y)
                y = -math.sin(rad) * (i - mid_x) + math.cos(rad) * (j - mid_y)

                if type == 'Nearest Neighbor':
                    # Rounds to get nearest neighbor
                    # Adding mid_x and mid_y for inverse translation back to original position
                    x = round(x) + mid_x
                    y = round(y) + mid_y
                    if x >= 0 and y >= 0 and x < width and y < height: interpolated = Rotation.t_array[x][y]

                else:
                    x += mid_x
                    y += mid_y
                    # Calling biinear in terpolation
                    interpolated = Interpolate.interpolate_bilinear(self, x, y, width, height, Rotation.t_array)

                # Crop out of original bounds pixels
                if x >= 0 and y >= 0 and x < width and y < height:
                    rotated_array[i][j] = interpolated

        Display.display_image(self, self.rotation_figure, rotated_array)


    def shear(self, value, type):
        # Create new array for sheared image
        sheared_array = np.zeros( (Rotation.t_array.shape), dtype=np.uint8)

        # Sheared array width and height
        width = sheared_array.shape[0]
        height = sheared_array.shape[1]

        # Center
        mid_x = width // 2
        mid_y = height // 2

        for i in range(height):
            for j in range(width):

                # Horizontal shearing
                x = i
                y = value * i + j

                if type == 'Nearest Neighbor':
                    x = round(x)
                    y = round(y - (value * mid_y))
                    if x >= 0 and y >= 0 and x < width and y < height: interpolated = Rotation.t_array[x][y]

                else:
                    y -= value * mid_y
                    if x >= 0 and y >= 0 and x < width and y < height: interpolated = Interpolate.interpolate_bilinear(self, x, y, width, height, Rotation.t_array)

                if x >= 0 and y >= 0 and x < width and y < height:
                    sheared_array[i][j] = interpolated


        Display.display_image(self, self.rotation_figure, sheared_array)