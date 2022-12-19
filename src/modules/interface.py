from PyQt5.QtGui import *
from numpy import rot90
from modules import openfile
from modules.size_interpolation import Interpolate
from modules.displays import Display
from modules.rotation_shear import RotationShear
from modules.noise_models import NoiseModels
import threading


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


    self.equalize_button.clicked.connect(
        lambda: self.histo.equalize(self)
    )
    # self.equalize_button.clicked.connect(
    #     lambda: self.disp.display_image(self.equalized_eq_figure, self.histo.equalized_image_array)
    # )
    # self.equalize_button.clicked.connect(
    #     lambda: self.disp.display_histo(self.equalized_histo_figure, self.histo.equalized_histogram_array)
    # )


    # Spatial Filtering
    self.salt_controls_widget.hide()
    self.unsharp_button.setEnabled(False)
    self.noise_button.setEnabled(False)

    self.unsharp_slider.valueChanged.connect(
        lambda: self.unsharp_slider.setValue(check_slider_val(self.unsharp_slider.value())))

    self.unsharp_slider.valueChanged.connect(
        lambda: self.unsharp_lcd.display(self.unsharp_slider.value()))

    self.boost_slider.valueChanged.connect(
        lambda: self.boost_lcd.display(self.boost_slider.value() / 10))

    self.unsharp_button.clicked.connect(
        lambda: self.unsharp.unsharp_masking(self, self.unsharp_slider.value(), self.boost_slider.value() / 10)
    )

    self.noise_button.clicked.connect(
        lambda: self.salt.add_saltandpepper(self, self.noise_percentage_spinBox.value() / 100)
    )

    self.noise_button.clicked.connect(
        lambda: self.noise_button.hide()
    )

    self.noise_button.clicked.connect(
        lambda: self.noise_percentage_spinBox.hide()
    )

    self.noise_button.clicked.connect(
        lambda: self.salt_controls_widget.show()
    )

    self.salt_slider.valueChanged.connect(
        lambda: self.salt_slider.setValue(check_slider_val(self.salt_slider.value())))

    self.salt_slider.valueChanged.connect(
        lambda: self.salt_lcd.display(self.salt_slider.value()))

    self.salt_button.clicked.connect(
        lambda: self.salt.apply_median_filter(self, self.salt_slider.value())
    )



    self.ff_kernel_slider.valueChanged.connect(
        lambda: self.ff_kernel_slider.setValue(check_slider_val(self.ff_kernel_slider.value())))
    self.ff_kernel_slider.valueChanged.connect(
        lambda: self.ff_lcd.display(self.ff_kernel_slider.value()))

    self.ff_apply.clicked.connect(
        lambda: threading.Thread(target=Display.display_image, args=(self, self.ff_spatial_figure, self.unsharp.apply_box_filter(self.ff_kernel_slider.value()))).start()
    )
    self.ff_apply.clicked.connect(
        lambda: self.freq_filter.apply_filter(self, self.ff_kernel_slider.value())
    )


    self.noise_removal_apply.clicked.connect(
        lambda: self.freq_mask.apply_mask(self)
    )




    self.noise_options.hide()
    self.uniform_options.hide()
    self.generate_phantom_button.clicked.connect(
        lambda: self.noise_model.create_phantom(self)
    )
    self.noise_combobox.currentIndexChanged.connect(
        lambda: noise_model_selection(self, self.noise_combobox.currentText())
    )
    # self.a_spinBox.valueChanged.connect(
    #     lambda: validate_a_b_values(self, self.a_spinBox.value(), self.b_spinBox.value())
    # )
    # self.b_spinBox.valueChanged.connect(
    #     lambda: validate_a_b_values(self, self.a_spinBox.value(), self.b_spinBox.value())
    # )
    self.phantom_noise_apply_button.clicked.connect(
        lambda: apply_noise_model(self, self.noise_combobox.currentText())
    )



    self.bp_lineEdit.hide()
    self.manual.hide() # Comment to add manual input
    self.start_spinBox.valueChanged.connect(
        lambda: self.end_spinBox.setMinimum(self.start_spinBox.value() + 1)
    )
    self.end_spinBox.valueChanged.connect(
        lambda: self.start_spinBox.setMaximum(self.end_spinBox.value() - 1)
    )
    self.manual.toggled.connect(
        lambda: manual_input_handler()
    )
    self.bp_apply.clicked.connect(
        lambda: calculate_lamino_handler()
    )


    def noise_model_selection(self, type):
        if type == 'Gaussian':
            self.gaussian_options.show()
            self.uniform_options.hide()
        elif type == 'Uniform':
            self.gaussian_options.hide()
            self.uniform_options.show()

    def apply_noise_model(self, type):
        if type == 'Gaussian':
            self.noise_model.add_noise(self, self.mean_spinBox.value(), self.sigma_spinBox.value(), type)
        elif type == 'Uniform':
            self.noise_model.add_noise(self, self.a_spinBox.value(), self.b_spinBox.value(), type)

    def validate_a_b_values(self, a, b):
        if a >= b:
            self.b_spinBox.setValue(a+1)

    def check_slider_val(value):
        if value % 2 == 0:
            return value - 1
        return value


    def manual_input_handler():

        if self.manual.isChecked():
            self.bp_lineEdit.show()
        else: 
            self.bp_lineEdit.hide()

    def calculate_lamino_handler():
        
        if self.manual.isChecked():
            self.back_projection.create_lamino_manual_entry(self.bp_lineEdit.text(), self.bp_filter_combobox.currentText())
        else: 
            self.back_projection.create_laminogram(self.start_spinBox.value(), self.end_spinBox.value(), self.step_spinBox.value(), self.bp_filter_combobox.currentText())