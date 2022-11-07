import numpy as np
from modules.displays import Display
import matplotlib.pylab as plt
import math

class HistogramEqualizer:
    
    depth = 256
    image_array = []
    histogram_array = []
    equalized_image_array = []
    equalized_histogram_array = []

    def __init__(self, arr, depth = 256):
        self.image_array = np.array(arr)
        self.depth = depth
        self.histogram_array = self.calculate_histo_array(self.image_array)
        print(np.amax(self.histogram_array))

    
    
    def calculate_histo_array(self, image):
        
        # Flatten image array
        flat = image.flatten()

        # Create array to store pixel value frequency
        histo_arr = np.zeros(self.depth, dtype=np.uint)

        # Loop over flat image and count
        for i in flat:
            histo_arr[i] = histo_arr[i] + 1

        # Divide by total number of pixels to get probabilities (noramlize)
        return histo_arr / self.image_array.size

    
    
    def calculate_cdf(self):
        ''' Calculate CDF '''
        cdf = np.zeros(len(self.histogram_array), dtype=np.float32)
        prev = 0
        for i in range(len(self.histogram_array)):
            cdf[i] = self.histogram_array[i] + prev
            prev = cdf[i]

        return cdf

    def equalize(self, mw):

        # Get CDF
        cdf = self.calculate_cdf()

        # Lookup map/table that returns the equalized value
        equalizer_map = np.round((self.depth - 1) * cdf).astype(np.uint8)

        # Pass in original pixel values to equalizer_map, returning the equalized values
        eq_flat = [equalizer_map[pixel] for pixel in self.image_array.flatten()]

        # flat_image = self.image_array.flatten()

        # eq = np.zeros(self.image_array.shape, dtype=np.uint)
        # eq_flat = eq.flatten()

        # for i in range(len(self.image_array.flatten())):
        #     eq_flat[i] = equalizer_map[flat_image[i]]
        
        # print(eq_flat)

        # Reshape equalized flat image to form new image array
        self.equalized_image_array = np.reshape(np.asarray(eq_flat), self.image_array.shape)

        # Calculate equalized image's histogram
        self.equalized_histogram_array = self.calculate_histo_array(self.equalized_image_array)

        Display.display_image(mw, mw.equalized_eq_figure, self.equalized_image_array)
        plt.axis('off')
        Display.display_histo(mw.equalized_histo_figure, self.equalized_histogram_array, self.depth)

        