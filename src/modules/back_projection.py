import skimage as skit
from skimage import transform, data
import numpy as np
from modules.displays import Display

class BackProjection:

    def __init__(self):
        # Generate shepp-logan phantom
        self.image_array = data.shepp_logan_phantom()
        # Convert it to np array
        self.image_array = np.array(self.image_array)
        # Display shepp-logan
        Display.display_image(Display.mw, Display.mw.shepp_logan_figure, self.image_array)
        # Create and display sinogram
        self.create_sinogram()


    def create_sinogram(self):
        # Angles from 0 --> 179
        theta = np.arange(0, 180, 1)
        # Create sinogram
        sinogram = transform.radon(self.image_array, theta)
        # Display sinogram
        Display.display_image(Display.mw, Display.mw.sinogram_figure, sinogram)

    def create_laminogram(self, start, end, step, filter):

        if filter == 'None': filter = None
        elif filter == 'Ram-Lak': filter = 'ramp'
        elif filter == 'Hamming': filter = 'hamming'
        # Angles from user input start --> end with given step
        theta = np.arange(start, end + 1, step)
        # Radon transform
        radon = transform.radon(self.image_array, theta)
        # Inverse radon transform to get laminogram, while applying given filter
        laminogram = transform.iradon(radon, theta, filter_name=filter)
        # Display laminogram
        Display.display_image(Display.mw, Display.mw.lamino_figure, laminogram)

    def create_lamino_manual_entry(self, arr, filter):
        
        if filter == 'None': filter = None
        elif filter == 'Ram-Lak': filter = 'ramp'
        elif filter == 'Hamming': filter = 'hamming'

        # Array of int from input
        arr = list(map(int, arr.split()))
        
        # Radon transform
        radon = transform.radon(self.image_array, arr)
        # Inverse radon transform to get laminogram, while applying given filter
        laminogram = transform.iradon(radon, arr, filter_name=filter)
        # Display laminogram
        Display.display_image(Display.mw, Display.mw.lamino_figure, laminogram)
