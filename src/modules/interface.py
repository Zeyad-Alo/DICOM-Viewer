from PyQt5.QtGui import *
from modules import openfile
from modules.size_interpolation import Interpolate


def init_connectors(self):
    self.actionOpen.triggered.connect(
        lambda: openfile.browse_window(self))

    self.size_slider.valueChanged.connect(
        lambda: self.size_lcd.display((self.size_slider.value()/10)))
        
    self.size_slider.sliderReleased.connect(
        lambda: Interpolate.interpolate_nearest_neighbor(self, (self.size_slider.value()/10)))
