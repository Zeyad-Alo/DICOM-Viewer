from PyQt5.QtWidgets import QFileDialog
from modules.displays import Display
from modules import image_data
from modules.size_interpolation import Interpolate
import numpy as np
from modules.equalization import HistogramEqualizer
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


        
        try:
            Display.display_image(self, self.main_figure, self.data.plot_data)
            Display.display_metadata(self, self.data.get_attributes())
        except:
            Display.clear_layout(self)
            Display.clear_image(self, self.main_figure)
            Display.clear_image(self, self.nn_figure)
            Display.clear_image(self, self.bilinear_figure)