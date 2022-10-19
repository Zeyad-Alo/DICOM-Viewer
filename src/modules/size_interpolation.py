import math
import numpy as np
from modules.displays import Display
import threading

class Interpolate:

    image_array = []
    

    # Calls both functions at once whenever slider changes with bilinear on a separate thread to examine time difference
    def interpolate(self, scale):
        Interpolate.interpolate_nearest_neighbor(self, scale)
        threading.Thread(target=Interpolate.interpolate_bilinear, args=(self, scale)).start()



    def interpolate_nearest_neighbor(self, scale):

        if len(Interpolate.image_array) > 0:
            new_w = math.ceil(Interpolate.image_array.shape[0] * scale)
            new_h = math.ceil(Interpolate.image_array.shape[1] * scale)
            # Create array with new sizes
            new_arr = np.zeros(shape=(new_w,new_h))
            # print(Interpolate.image_array.shape[0], Interpolate.image_array.shape[1])
            # print(new_w, new_h)

            for i in range(new_w):
                for j in range(new_h):
                    new_arr[i][j] = Interpolate.image_array[math.floor(i/scale)][math.floor(j/scale)]

            # Resize plot to make it scrollable
            self.nn_plot.resize(new_arr.shape[1],new_arr.shape[0])

            Display.display_image(self, self.nn_figure, new_arr)

            # Show resized dimensions
            self.resized_label.setText(str(new_arr.shape[1]) + 'x' + str(new_arr.shape[0]))


        else: return


    def interpolate_bilinear(self, scale):
        if len(Interpolate.image_array) > 0:
            in_w = Interpolate.image_array.shape[0]
            in_h = Interpolate.image_array.shape[1]
            new_w = math.ceil(in_w * scale)
            new_h = math.ceil(in_h * scale)
            # Create array with new sizes
            new_arr = np.zeros(shape=(new_w,new_h))

            for i in range(new_w):
                for j in range(new_h):
                    # Relative coordinates of the pixel in output space
                    x_out = i / new_w
                    y_out = j / new_h

                    # Corresponding absolute coordinates of the pixel in input space
                    x_in = (x_out * in_w)
                    y_in = (y_out * in_h)

                    # Nearest neighbours coordinates in input space
                    x_prev = int(np.floor(x_in))
                    x_next = x_prev + 1
                    y_prev = int(np.floor(y_in))
                    y_next = y_prev + 1

                    # Push coorinates out of bounds of input array back to the edges
                    x_prev = min(x_prev, in_w - 1)
                    x_next = min(x_next, in_w - 1)
                    y_prev = min(y_prev, in_h - 1)
                    y_next = min(y_next, in_h - 1)
                    
                    # Distances between neighbour nodes in input space
                    Dy_next = y_next - y_in
                    Dy_prev = 1 - Dy_next; # because next - prev = 1
                    Dx_next = x_next - x_in
                    Dx_prev = 1 - Dx_next; # because next - prev = 1
                    
                    new_arr[i][j] = Dy_prev * (Interpolate.image_array[x_prev][y_next] * Dx_next + Interpolate.image_array[x_next][y_next] * Dx_prev) \
                    + Dy_next * (Interpolate.image_array[x_prev][y_prev] * Dx_next + Interpolate.image_array[x_next][y_prev] * Dx_prev)

            # Resize plots to make it scrollable
            self.bilinear_plot.resize(new_arr.shape[1],new_arr.shape[0])

            Display.display_image(self, self.bilinear_figure, new_arr)

        else: return
