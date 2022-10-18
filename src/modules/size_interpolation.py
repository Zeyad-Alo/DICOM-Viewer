import math
from matplotlib.pyplot import sca
import numpy as np
from modules.displays import Display

class Interpolate:
    # scale = 1

    # def __init__(self, image_array):
    #     self.image_array = image_array

    image_array = []

    def interpolate_nearest_neighbor(self, scale):

        if len(Interpolate.image_array) > 0:
            new_w = math.ceil(Interpolate.image_array.shape[0] * scale)
            new_h = math.ceil(Interpolate.image_array.shape[1] * scale)
            # Create array with new sizes
            new_arr = np.zeros(shape=(new_w,new_h))
            print(Interpolate.image_array.shape[0], Interpolate.image_array.shape[1])
            print(new_w, new_h)

            for i in range(new_w):
                for j in range(new_h):
                    new_arr[i][j] = Interpolate.image_array[math.floor(i/scale)][math.floor(j/scale)]

            Display.display_image(self, self.nn_figure, new_arr)

        else: return


    def interpolate_bilinear():
        pass
