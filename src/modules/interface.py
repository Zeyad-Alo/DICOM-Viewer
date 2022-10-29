from PyQt5.QtGui import *
from numpy import rot90
from modules import openfile
from modules.size_interpolation import Interpolate
from modules.rotation import Rotation
import numpy as np


# UI connectors
def init_connectors(self):

    # Open file button
    self.actionOpen.triggered.connect(
        lambda: openfile.browse_window(self))

    # Size slider and lcd
    self.size_slider.valueChanged.connect(
        lambda: self.size_lcd.display((self.size_slider.value()/10)))

    self.size_slider.sliderReleased.connect(
        lambda: Interpolate.interpolate(self, (self.size_slider.value()/10)))


    # Rotation
    self.controls_widget.hide()

    self.construct_button.clicked.connect(
        lambda: Rotation.construct_t(self)
    )
    self.construct_button.clicked.connect(
        lambda: self.construct_button.hide()
    )
    self.construct_button.clicked.connect(
        lambda: self.controls_widget.show()
    )
    
    self.rotation_slider.valueChanged.connect(
        lambda: self.rotation_lcd.display(self.rotation_slider.value()))
    self.rotation_slider.valueChanged.connect(
        lambda: Rotation.rotate(self, self.rotation_slider.value(), self.interpolation_comboBox.currentText()))

    self.interpolation_comboBox.currentIndexChanged.connect(
        lambda: Rotation.rotate(self, self.rotation_slider.value(), self.interpolation_comboBox.currentText()))

    # self.rotation_slider.valueChanged.connect(
    #     lambda: Rotation.shear(self, self.rotation_slider.value() / 10, self.interpolation_comboBox.currentText()))

    # self.interpolation_comboBox.currentIndexChanged.connect(
    #     lambda: Rotation.shear(self, self.rotation_slider.value() / 10, self.interpolation_comboBox.currentText()))
