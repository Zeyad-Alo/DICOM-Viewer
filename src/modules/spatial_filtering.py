import numpy as np
from modules.displays import Display
import matplotlib.pylab as plt
import random

class UnsharpMasking:

    image_array = []
    unsharp_kernel_size = 0
    blurred_image_array = []

    def __init__(self, array):
        self.image_array = array

    def pad_image(arr, kernel):
        '''
        Adds zero padding to image to accomodate for kernel size
        '''
        # Offset of image placement inside padded array
        offset_x = kernel[0] // 2
        offset_y = kernel[1] // 2

        # Padded array's dimensions
        new_arr_width = arr.shape[1] + kernel - 1
        new_arr_height = arr.shape[0] + kernel - 1
        
        # Initialize empty array
        padded_array = np.zeros(shape=(new_arr_height, new_arr_width), dtype=np.uint)

        # Insert image into padded array
        padded_array[offset_x:offset_x+arr.shape[0], offset_y:offset_y+arr.shape[1]] = arr
        return padded_array


    def apply_box_filter(self, size):
        '''
        Creates blurred image using a box filter with size set by user
        '''
        # Create box kernel filled with 1s
        box_kernel = np.ones(shape=(size,size))

        # Get padded image
        padded_array = self.pad_image(self.image_array, (size,size))

        # Initialize output array
        output_array = np.zeros(self.image_array.shape)

        # Offsets of start and end of original image with respect to padded image
        offset = size // 2
        rows_stop = offset + self.image_array.shape[0]
        col_stop = offset + self.image_array.shape[1]

        # Loop over padded image and calculate output of box filter at each pixel
        for x in range(offset, rows_stop):
            for y in range(offset, col_stop):
                mask = padded_array[x-offset:x+offset+1, y-offset:y+offset+1]       # This is the local sub-image that lies under the kernel
                output_array[x-offset][y-offset] = round(self.matrix_sum(box_kernel, mask) / (size ** 2))      # Calculate sum of kernel * mask and divide by kernel size

        self.blurred_image_array = output_array
        return output_array


    def unsharp_masking(self, mw, size, k=1):
        '''
        Calculates and displays the unsharped mask of the image according to
        user input
        '''
        # Set kernel size
        self.unsharp_kernel_size = size

        # Get blurred image
        blurred = self.apply_box_filter(size)

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

    def add_saltandpepper(self, mw, weight):
        '''
        Randomly adds salt and pepper noise over image
        '''
        # Loop over image and add noise according to random conditions
        for i in range(self.image_array.shape[0]):
            for j in range(self.image_array.shape[1]):

                if random.uniform(0,1) < weight:
                    noise_value = random.randint(0,1)       # Whether to add salt or pepper
                    self.salty_image_array[i][j] = noise_value * 255
                else:
                    self.salty_image_array[i][j] = self.image_array[i][j]

        Display.display_image(mw, mw.salt_figure, self.salty_image_array)
        plt.axis('off')


    def apply_median_filter(self, mw, size):

        # Initialize output array
        out_array = np.zeros(shape=self.salty_image_array.shape, dtype=np.uint)

        # Get padded image
        padded_array = UnsharpMasking.pad_image(self, self.salty_image_array, (size, size))

        # Offsets of start and end of original image with respect to padded image
        offset = size // 2
        rows_stop = offset + self.salty_image_array.shape[0]
        col_stop = offset + self.salty_image_array.shape[1]

        # Loop over padded image and calculate output of median filter at each pixel
        for x in range(offset, rows_stop):
            for y in range(offset, col_stop):
                local = padded_array[x-offset:x+offset+1, y-offset:y+offset+1]       # This is the local sub-image that lies under the kernel
                
                # Sort local sub-image and replace pixel with median
                b = local.flatten()
                merge_sort(local.flatten(), b, 0, len(local.flatten()) - 1)
                out_array[x-offset][y-offset] = b[len(b) // 2]

        Display.display_image(mw, mw.salt_figure, out_array)
        plt.axis('off')




def merge_sort(a, b, left, right):
    '''
    Uses divide and conquer merge sort algorithm to effeciently count number of inversions,
    improves time complexity to O(nlogn)
    '''
    
    # Return if size becomes <= 1
    if right <= left:
        return

    # Find midpoint
    mid = (left + right)//2

    # Split array recursively into halves and merge them upwards again
    merge_sort(a, b, left, mid)
    merge_sort(a, b, mid + 1, right)
    merge(a, b, left, mid, right)


def merge(a, b, left, mid, right):
    i = left     # Starting index of left subarray
    j = mid + 1  # Starting index of right subarray
    k = left
 
    while i <= mid and j <= right:    # Make sure i and j do not exceed array limits
    
        # Compare elements, invert if needed, and increment to the next element
        if a[i] <= a[j]:
            b[k] = a[i]
            i += 1
        else:
            # Count inversion
            b[k] = a[j]
            j += 1
 
        k += 1

    # Copy the remaining elements of left and right arrays to the temp array
    while i <= mid:
        b[k] = a[i]
        k += 1
        i += 1

    while j <= right:
        b[k] = a[j]
        k += 1
        j += 1
 
    # Copy the sorted subarray into the original array
    for i in range(left, right + 1):
        a[i] = b[i]