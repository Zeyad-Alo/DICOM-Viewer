import numpy as np
from modules.displays import Display
import matplotlib.pylab as plt
import random

class UnsharpMasking:

    image_array = []
    unsharp_kernel_size = 0

    def __init__(self, array):
        self.image_array = array

    def pad_image(self):
        '''
        Adds zero padding to image to accomodate for kernel size
        '''
        # Number of pad rows/columns needed around image
        pad = self.unsharp_kernel_size // 2
        
        # Pad image and return in new array
        padded_array = np.pad(self.image_array, [(pad, pad), (pad, pad)], mode='constant', constant_values=0)
        return padded_array


    def apply_box_filter(self):
        '''
        Creates blurred image using a box filter with size set by user
        '''
        # Create box kernel filled withed 1s
        box_kernel = np.ones(shape=(self.unsharp_kernel_size,self.unsharp_kernel_size))

        # Get padded image
        padded_array = self.pad_image()

        # Initialize output array
        output_array = np.zeros(self.image_array.shape)

        # Offsets of start and end of original image with respect to padded image
        offset = self.unsharp_kernel_size // 2
        rows_stop = offset + self.image_array.shape[0]
        col_stop = offset + self.image_array.shape[1]

        # Loop over padded image and calculate output of box filter at each pixel
        for x in range(offset, rows_stop):
            for y in range(offset, col_stop):
                mask = padded_array[x-offset:x+offset+1, y-offset:y+offset+1]       # This is the local sub-image that lies under the kernel
                output_array[x-offset][y-offset] = round(self.matrix_sum(box_kernel, mask) / (self.unsharp_kernel_size ** 2))      # Calculate sum of kernel * mask and divide by kernel size

        return output_array


    def unsharp_masking(self, mw, size, k=1):
        '''
        Calculates and displays the unsharped mask of the image according to
        user input
        '''
        # Set kernel size
        self.unsharp_kernel_size = size

        # Get blurred image
        blurred = self.apply_box_filter()

        # Subtract blurred from original
        diff = self.image_array - blurred

        # Add difference to original with highboost factor
        unsharp = self.image_array + k * diff

        # Scale to retain 0-255 intensity range OR Clip out of range pixels to thresholds
        # unsharp = self.intensity_scaling(unsharp)
        unsharp = self.intensity_clipping(unsharp)

        Display.display_image(mw, mw.unsharp_figure, unsharp)
        plt.axis('off')


    def matrix_sum(self, kernel, sub):
        '''
        Convolves the kernel with the underlaying local sub-image
        '''
        sum = 0
        kernel = kernel.flatten()
        sub = sub.flatten()

        for i in range(len(kernel)):
                sum += kernel[i]*sub[i]

        return sum


    '''
    To handle intensity values going out of range, we can either
    scale all intensities into range, or clip out of range ones.
    However, clipping produces better looking results and sharper images.
    '''
    def intensity_scaling(self, arr):
        # Shift all intensities so that min value --> 0
        arr = arr - np.amin(arr)
        # Normalize intesities and scale them to max of 255
        arr = np.round((arr / np.amax(arr)) * 255)
        return arr

    def intensity_clipping(self, arr):
        arr[arr < 0] = 0
        arr[arr > 255] = 255
        return arr






class ImpulseNoise:

    image_array = []
    salty_image_array = []

    def __init__(self, array):
        self.image_array = array
        self.salty_image_array = np.zeros(shape=self.image_array.shape, dtype=np.uint)

    def add_saltandpepper(self, mw):
        '''
        Randomly adds salt and pepper noise over image
        '''
        # Loop over image and add noise according to random conditions
        for i in range(self.image_array.shape[0]):
            for j in range(self.image_array.shape[1]):

                add_noise = random.randint(0,1)     # Whether to add noise in this pixel or leave it as is

                if add_noise == 1:
                    noise_value = random.randint(0,1)       # Whether to add salt or pepper
                    self.salty_image_array[i][j] = noise_value * 255
                else:
                    self.salty_image_array[i][j] = self.image_array[i][j]

        Display.display_image(mw, mw.salt_figure, self.salty_image_array)
        plt.axis('off')


    def pad_image(self, size):
        '''
        Adds zero padding to image to accomodate for kernel size
        '''
        # Number of pad rows/columns needed around image
        pad = size // 2
        
        # Pad image and return in new array
        padded_array = np.pad(self.salty_image_array, [(pad, pad), (pad, pad)], mode='constant', constant_values=0)
        return padded_array


    def apply_median_filter(self, mw, size):

        # Initialize output array
        out_array = np.zeros(shape=self.salty_image_array.shape, dtype=np.uint)

        # Get padded image
        padded_array = self.pad_image(size)

        # Offsets of start and end of original image with respect to padded image
        offset = size // 2
        rows_stop = offset + self.salty_image_array.shape[0]
        col_stop = offset + self.salty_image_array.shape[1]

        # Loop over padded image and calculate output of median filter at each pixel
        for x in range(offset, rows_stop):
            for y in range(offset, col_stop):
                mask = padded_array[x-offset:x+offset+1, y-offset:y+offset+1]       # This is the local sub-image that lies under the kernel
                out_array[x-offset][y-offset] = np.median(mask.flatten())

        Display.display_image(mw, mw.salt_figure, out_array)
        plt.axis('off')
