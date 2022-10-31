from PyQt5.QtGui import *
from numpy import rot90
from modules import openfile
from modules.size_interpolation import Interpolate
from modules.rotation_shear import RotationShear
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
    self.r_controls_widget.hide()

    self.r_construct_button.clicked.connect(
        lambda: RotationShear.construct_t(self, 'r')
    )
    self.r_construct_button.clicked.connect(
        lambda: self.r_construct_button.hide()
    )
    self.r_construct_button.clicked.connect(
        lambda: self.r_controls_widget.show()
    )
    
    self.rotation_slider.valueChanged.connect(
        lambda: self.rotation_lcd.display(self.rotation_slider.value()))
    self.rotation_slider.valueChanged.connect(
        lambda: RotationShear.rotate(self, self.rotation_slider.value(), self.r_interpolation_comboBox.currentText()))

    self.r_interpolation_comboBox.currentIndexChanged.connect(
        lambda: RotationShear.rotate(self, self.rotation_slider.value(), self.r_interpolation_comboBox.currentText()))


    # Shear
    self.s_controls_widget.hide()

    self.s_construct_button.clicked.connect(
        lambda: RotationShear.construct_t(self, 's')
    )
    self.s_construct_button.clicked.connect(
        lambda: self.s_construct_button.hide()
    )
    self.s_construct_button.clicked.connect(
        lambda: self.s_controls_widget.show()
    )
    
    self.shear_slider.valueChanged.connect(
        lambda: self.shear_lcd.display(self.shear_slider.value()))
    self.shear_slider.valueChanged.connect(
        lambda: RotationShear.shear(self, self.shear_slider.value(), self.s_interpolation_comboBox.currentText()))

    self.s_interpolation_comboBox.currentIndexChanged.connect(
        lambda: RotationShear.shear(self, self.shear_slider.value(), self.s_interpolation_comboBox.currentText()))
