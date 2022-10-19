from PyQt5.QtWidgets import QFileDialog
from modules import interface
from modules.displays import Display
from modules import image_data
from modules.size_interpolation import Interpolate
import numpy as np

def browse_window(self):

    self.filename = QFileDialog.getOpenFileName(
        None, 'open the image file', './', filter="Raw Data(*.bmp *.jpg *.png *.dcm)")

    path = self.filename[0]

    if path != '':

        # Reset slider position
        self.size_slider.setValue(10)
        
        data = image_data.ImageData(path)
        Interpolate.image_array = np.array(data.grayscale_img)
        Interpolate.interpolate_nearest_neighbor(self, (self.size_slider.value()/10))
        Interpolate.interpolate_bilinear(self, (self.size_slider.value()/10))

        
        try:
            Display.display_image(self, self.main_figure, data.plot_data)
            Display.display_metadata(self, data.get_attributes())
        except:
            Display.clear_layout(self)
            Display.clear_image(self, self.main_figure)
            Display.clear_image(self, self.nn_figure)
            Display.clear_image(self, self.bilinear_figure)