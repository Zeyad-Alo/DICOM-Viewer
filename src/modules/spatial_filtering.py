import numpy as np
from modules.displays import Display
import matplotlib.pylab as plt

class Unsharp:

    image_array = []
    n_filter = 0

    def __init__(self, array):
        self.image_array = array

    def pad_image(self):
        pad = self.n_filter // 2
        padded_array = np.pad(self.image_array, [(pad, pad), (pad, pad)], mode='constant', constant_values=0)
        return padded_array


    def apply_box_filter(self):

        box_kernel = np.ones(shape=(self.n_filter,self.n_filter), dtype=np.uint8)
        padded_array = self.pad_image()
        output_array = np.zeros(self.image_array.shape, dtype=np.int)

        offset = self.n_filter // 2
        rows_stop = self.n_filter // 2 + self.image_array.shape[0]
        col_stop = self.n_filter // 2 + self.image_array.shape[1]

        for x in range(offset, rows_stop):
            for y in range(offset, col_stop):

                mask = padded_array[x-offset:x+offset+1, y-offset:y+offset+1]
                output_array[x-offset][y-offset] = round(self.matrix_sum(box_kernel, mask) / self.n_filter ** 2)

        return output_array

    def unsharp_filter(self, mw, size, k=1):
        self.n_filter = size
        blurred = self.apply_box_filter()
        diff = self.image_array - blurred
        print(diff)
        diff = self.intensity_scaling(diff)
        unsharp = self.image_array + k * diff
        # print(unsharp)
        # unsharp = self.intensity_scaling(diff)
        Display.display_image(mw, mw.unsharp_figure, unsharp)
        plt.axis('off')
        return unsharp



    def matrix_sum(self, kernel, mask):
        sum = 0
        kernel = kernel.flatten()
        mask = mask.flatten()

        for i in range(len(kernel)):
                sum += kernel[i]*mask[i]

        return sum


    def intensity_scaling(self, arr):
        arr = arr - np.amin(arr)
        arr = np.round((arr / np.amax(arr)) * 255)
        return arr