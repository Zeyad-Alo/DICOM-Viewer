import skimage as skit
from skimage import transform, data
import numpy as np
from modules.displays import Display
from modules.rotation_shear import RotationShear

class BackProjection:

    def __init__(self):
        # Generate shepp-logan phantom
        self.image_array = transform.resize(data.shepp_logan_phantom(), (256, 256))
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

        # Create sinogram manually
        # sinogram = BackProjection.manual_radon_transform(self.image_array, theta)
        
        # Display sinogram
        Display.display_image(Display.mw, Display.mw.sinogram_figure, sinogram)
    
    
    def manual_radon_transform(image, theta):
        sinogram = np.zeros((image.shape[0], len(theta)))

        for step in range(len(theta)):
            # Rotate image with each angle in theta array
            rotated_image = RotationShear.rotate(image, -theta[step], 'bl')

            # 1D array of summed columns from rotated image --> projection
            radon_projection = sum(rotated_image)

            # Set corresponding row of sinogram array with this projection
            sinogram[:,step] = radon_projection

        return sinogram


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
