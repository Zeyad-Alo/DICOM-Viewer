import numpy as np

class ImageFFT:

    image_array = []
    image_fft_array = []
    image_fft_mag_array = []
    image_fft_phase_array = []

    def __init__(self, arr):
        self.image_array = arr
        self.image_fft_array = np.fft.fft2(self.image_array)
        shifted_fft_array = np.fft.fftshift(self.image_fft_array)
        
        self.image_fft_mag_array = np.sqrt(shifted_fft_array.real ** 2 + shifted_fft_array.imag ** 2)
        self.image_fft_phase_array = np.arctan2(shifted_fft_array.imag, shifted_fft_array.real)
