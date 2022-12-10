import numpy as np
from modules.displays import Display

class FrequencyFilter:

    def __init__(self, image):
        # ImageFFT class object
        self.image = image

    def create_filter(self, size):
        
        # Spatial box filter
        kernel = np.ones(shape=(size, size), dtype=np.uint) / size ** 2

        # Zeros array used in padding the kernel
        padded_kernel = np.zeros(shape=self.image.image_array.shape)

        # Offsets of kernel in zeros array to center it
        x_offset = (self.image.image_array.shape[0] - kernel.shape[0]) // 2
        y_offset = (self.image.image_array.shape[1] - kernel.shape[1]) // 2

        # Place kernel in center of zeros array hence padding it
        padded_kernel[x_offset:x_offset + kernel.shape[0], y_offset:y_offset + kernel.shape[1]] = kernel

        # ifftshift the centered kernel to account for spatial phase difference
        padded_kernel = np.fft.ifftshift(padded_kernel)
        # Apply fft
        filter_fft = np.fft.fft2(padded_kernel)

        return filter_fft

    def apply_filter(self, mw, size):

        # Create filter and transform it to frequency domain
        filter_fft = self.create_filter(size)

        # Multiply image with filter in frequency domain
        filtered_fft_image = self.image.image_fft_array * filter_fft

        # Transform back to spatial domain while only getting real component and converting it back to 8 bits
        filtered_image = np.fft.ifft2(filtered_fft_image).real
        filtered_image = filtered_image.astype(np.uint8)

        # Subtract image blurred in spatial domain from image blurred in frequency domain
        diff = filtered_image - mw.unsharp.blurred_image_array

        Display.display_image(mw, mw.ff_freq_figure, filtered_image)
        Display.display_image(mw, mw.ff_diff_figure, diff)

        return filtered_image


    

class FrequencyMask:

    def __init__(self, image_fft_array):
        self.image_fft_array = np.fft.fftshift(image_fft_array)
        self.mask = np.ones(shape=(self.image_fft_array.shape))

    def edit_mask(self, x0, y0, x1, y1):
        # Set selected values with 0 and keep rest of mask 1s
        self.mask[y0:y1, x0:x1] = 0

    def apply_mask(self, mw):

        # Multiply image with mask
        filtered_image_freq = self.image_fft_array * self.mask

        # Inverse shift and apply ifft
        filtered_image_spatial = np.fft.ifftshift(filtered_image_freq)
        filtered_image_spatial = np.fft.ifft2(filtered_image_spatial).real
        
        Display.display_image(mw, mw.noise_removal_after_mag_figure, np.log(np.abs(filtered_image_freq)+1))
        Display.display_image(mw, mw.noise_removal_after_figure, filtered_image_spatial)