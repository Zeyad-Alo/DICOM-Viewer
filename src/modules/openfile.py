from PyQt5.QtWidgets import QFileDialog
from modules.displays import Display
from modules import image_data
from modules.size_interpolation import Interpolate
import numpy as np
from modules.equalization import HistogramEqualizer
from modules.spatial_filtering import UnsharpMasking, ImpulseNoise
from modules.fourier import ImageFFT
import matplotlib.pylab as plt

def browse_window(self):

    self.filename = QFileDialog.getOpenFileName(
        None, 'open the image file', './', filter="Raw Data(*.bmp *.jpg *.png *.dcm *.jpeg)")

    path = self.filename[0]

    if path != '':

        # Reset slider position
        self.size_slider.setValue(10)
        
        self.data = image_data.ImageData(path)

        Interpolate.image_array = np.array(self.data.grayscale_img)
        Interpolate.interpolate(self, (self.size_slider.value()/10))

        # if np.amax(self.data.grayscale_img) <= 256:
        print(self.data.grayscale_depth)
        self.histo = HistogramEqualizer(self.data.grayscale_img, self.data.grayscale_depth)
        Display.display_image(self, self.original_eq_figure, self.histo.image_array)
        plt.axis('off')
        Display.display_histo(self.original_histo_figure, self.histo.histogram_array, self.data.grayscale_depth)
        Display.clear_image(self.equalized_eq_figure)
        Display.clear_image(self.equalized_histo_figure)


        self.unsharp_button.setEnabled(True)
        self.noise_button.setEnabled(True)
        self.unsharp = UnsharpMasking(self.data.grayscale_img)
        Display.display_image(self, self.unsharp_figure, self.unsharp.image_array)
        plt.axis('off')

        self.salt = ImpulseNoise(self.data.grayscale_img)
        Display.display_image(self, self.salt_figure, self.salt.image_array)
        plt.axis('off')
        self.salt_controls_widget.hide()
        self.noise_button.show()
        self.noise_percentage_spinBox.show()


        self.fourier = ImageFFT(self.data.grayscale_img)
        Display.display_image(self, self.pre_mag_figure, self.fourier.image_fft_mag_array)
        plt.axis('off')
        Display.display_image(self, self.pre_phase_figure, self.fourier.image_fft_phase_array)
        plt.axis('off')
        Display.display_image(self, self.post_mag_figure, np.log(self.fourier.image_fft_mag_array + 1))
        plt.axis('off')
        Display.display_image(self, self.post_phase_figure, np.log(self.fourier.image_fft_phase_array + np.pi))
        plt.axis('off')



        
        try:
            Display.display_image(self, self.main_figure, self.data.plot_data)
            Display.display_metadata(self, self.data.get_attributes())
        except:
            Display.clear_layout(self)
            Display.clear_image(self, self.main_figure)
            Display.clear_image(self, self.nn_figure)
            Display.clear_image(self, self.bilinear_figure)