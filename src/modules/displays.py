
from turtle import radians
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pylab as plt
import numpy as np
from matplotlib.patches  import Rectangle
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


plt.rcParams['axes.facecolor'] = 'black'
plt.rc('axes', edgecolor='w')
plt.rc('xtick', color='w')
plt.rc('ytick', color='w')
plt.rcParams["figure.autolayout"] = True

class Display:

    mw = None

    # CREATE BASE MATPLOTLIB CANVASES - CALLED ONCE ON LAUNCH
    def __init__(self, mw):
        self.mw = mw
        Display.create_main_canvas(self.mw)
        Display.create_neaarest_neighbor_canvas(self.mw)
        Display.create_bilinear_canvas(self.mw)
        Display.create_rotation_canvas(self.mw)
        Display.create_shear_canvas(self.mw)
        Display.create_equalization_canvas(self.mw)
        Display.create_unsharp_canvas(self.mw)
        Display.create_salt_canvas(self.mw)
        Display.create_pre_mag_canvas(self.mw)
        Display.create_pre_phase_canvas(self.mw)
        Display.create_post_mag_canvas(self.mw)
        Display.create_post_phase_canvas(self.mw)
        Display.create_ff_original_canvas(self.mw)
        Display.create_ff_spatial_canvas(self.mw)
        Display.create_ff_freq_canvas(self.mw)
        Display.create_ff_diff_canvas(self.mw)
        Display.create_noise_removal_og_canvas(self.mw)
        Display.create_noise_removal_og_mag_canvas(self.mw)
        Display.create_noise_removal_after_canvas(self.mw)
        Display.create_noise_removal_after_mag_canvas(self.mw)
        Display.create_phantom_canvas(self.mw)
        Display.create_phantom_noise_canvas(self.mw)
        Display.create_phantom_histo_canvas(self.mw)

        # Main
    def create_main_canvas(self):
        self.main_figure = plt.figure()
        self.main_figure.patch.set_facecolor('black')
        self.main_plot = Canvas(self.main_figure)
        self.image_box.addWidget(self.main_plot)


        # Resize
    def create_neaarest_neighbor_canvas(self):
        self.nn_scroll = QScrollArea()
        self.nn_scroll.setStyleSheet("background-color: black")

        self.nn_figure = plt.figure()
        self.nn_figure.patch.set_facecolor('black')
        self.nn_plot = Canvas(self.nn_figure)

        self.nn_scroll.setWidget(self.nn_plot)
        self.nearest_neighbor_box.addWidget(self.nn_scroll)

    def create_bilinear_canvas(self):
        self.bl_scroll = QScrollArea()
        self.bl_scroll.setStyleSheet("background-color: black")

        self.bilinear_figure = plt.figure()
        self.bilinear_figure.patch.set_facecolor('black')
        self.bilinear_plot = Canvas(self.bilinear_figure)
        
        self.bl_scroll.setWidget(self.bilinear_plot)
        self.bilinear_box.addWidget(self.bl_scroll)


        # Rotation and shear
    def create_rotation_canvas(self):
        self.rotation_figure = plt.figure()
        self.rotation_figure.patch.set_facecolor('black')
        self.axes = self.rotation_figure.add_subplot()
        self.rotation_plot = Canvas(self.rotation_figure)
        self.t_box_r.addWidget(self.rotation_plot)
        
    def create_shear_canvas(self):
        self.shear_figure = plt.figure()
        self.shear_figure.patch.set_facecolor('black')
        self.axes = self.shear_figure.add_subplot()
        self.shear_plot = Canvas(self.shear_figure)
        self.t_box_s.addWidget(self.shear_plot)


    def create_equalization_canvas(self):
        self.original_eq_figure = plt.figure()
        self.original_eq_figure.patch.set_facecolor('black')
        self.original_eq_plot = Canvas(self.original_eq_figure)
        self.original_image_box_e.addWidget(self.original_eq_plot)

        self.equalized_eq_figure = plt.figure()
        self.equalized_eq_figure.patch.set_facecolor('black')
        self.equalized_eq_plot = Canvas(self.equalized_eq_figure)
        self.equalized_image_box.addWidget(self.equalized_eq_plot)

        self.original_histo_figure = plt.figure()
        self.original_histo_figure.patch.set_facecolor('black')
        self.original_histo_plot = Canvas(self.original_histo_figure)
        self.original_histo_box.addWidget(self.original_histo_plot)

        self.equalized_histo_figure = plt.figure()
        self.equalized_histo_figure.patch.set_facecolor('black')
        self.equalized_histo_plot = Canvas(self.equalized_histo_figure)
        self.equalized_histo_box.addWidget(self.equalized_histo_plot)


    # Spatial Filtering
    def create_unsharp_canvas(self):
        self.unsharp_figure = plt.figure()
        self.unsharp_figure.patch.set_facecolor('black')
        self.unsharp_plot = Canvas(self.unsharp_figure)
        self.unsharp_box.addWidget(self.unsharp_plot)

    def create_salt_canvas(self):
        self.salt_figure = plt.figure()
        self.salt_figure.patch.set_facecolor('black')
        self.salt_plot = Canvas(self.salt_figure)
        self.salt_box.addWidget(self.salt_plot)


    
    # Fourier
    def create_pre_mag_canvas(self):
        self.pre_mag_figure = plt.figure()
        self.pre_mag_figure.patch.set_facecolor('black')
        self.pre_mag_plot = Canvas(self.pre_mag_figure)
        self.pre_mag_box.addWidget(self.pre_mag_plot)

    def create_pre_phase_canvas(self):
        self.pre_phase_figure = plt.figure()
        self.pre_phase_figure.patch.set_facecolor('black')
        self.pre_phase_plot = Canvas(self.pre_phase_figure)
        self.pre_phase_box.addWidget(self.pre_phase_plot)

    x0 = None
    y0 = None
    x1 = None
    y1 = None
    rect = None
    is_pressed = False

    def on_press(event):
        if not Display.mw.toolbar._actions['zoom'].isChecked():
            Display.is_pressed = True
            Display.x0 = event.xdata
            Display.y0 = event.ydata
            Display.rect = Rectangle((Display.x0, Display.y0), 0, 0)
            Display.rect.set_color('r')
            Display.rect.set_alpha(0.3)
            Display.mw.noise_removal_og_mag_figure.gca().add_patch(Display.rect)
            print('you pressed', event.button, event.xdata, event.ydata)

    def on_motion(event):
        if Display.is_pressed == True:
            Display.x1 = event.xdata
            Display.y1 = event.ydata
            Display.rect.set_width(event.xdata - Display.x0)
            Display.rect.set_height(event.ydata - Display.y0)
            Display.mw.noise_removal_og_mag_plot.draw()

    def on_release(event):
        Display.is_pressed = False
        Display.mw.freq_mask.edit_mask(round(Display.x0), round(Display.y0), round(Display.x1), round(Display.y1))
        print('you released', event.button, event.xdata, event.ydata)

    def create_post_mag_canvas(self):
        self.post_mag_figure = plt.figure()
        self.post_mag_figure.patch.set_facecolor('black')
        self.post_mag_plot = Canvas(self.post_mag_figure)
        self.post_mag_box.addWidget(self.post_mag_plot)



    def create_post_phase_canvas(self):
        self.post_phase_figure = plt.figure()
        self.post_phase_figure.patch.set_facecolor('black')
        self.post_phase_plot = Canvas(self.post_phase_figure)
        self.post_phase_box.addWidget(self.post_phase_plot)



    def create_ff_original_canvas(self):
        self.ff_original_figure = plt.figure()
        self.ff_original_figure.patch.set_facecolor('black')
        self.ff_original_plot = Canvas(self.ff_original_figure)
        self.ff_original_box.addWidget(self.ff_original_plot)

    def create_ff_spatial_canvas(self):
        self.ff_spatial_figure = plt.figure()
        self.ff_spatial_figure.patch.set_facecolor('black')
        self.ff_spatial_plot = Canvas(self.ff_spatial_figure)
        self.ff_spatial_box.addWidget(self.ff_spatial_plot)

    def create_ff_freq_canvas(self):
        self.ff_freq_figure = plt.figure()
        self.ff_freq_figure.patch.set_facecolor('black')
        self.ff_freq_plot = Canvas(self.ff_freq_figure)
        self.ff_freq_box.addWidget(self.ff_freq_plot)

    def create_ff_diff_canvas(self):
        self.ff_diff_figure = plt.figure()
        self.ff_diff_figure.patch.set_facecolor('black')
        self.ff_diff_plot = Canvas(self.ff_diff_figure)
        self.ff_diff_box.addWidget(self.ff_diff_plot)



    def create_noise_removal_og_canvas(self):
        self.noise_removal_og_figure = plt.figure()
        self.noise_removal_og_figure.patch.set_facecolor('black')
        self.noise_removal_og_plot = Canvas(self.noise_removal_og_figure)
        self.noise_removal_og_box.addWidget(self.noise_removal_og_plot)

    def create_noise_removal_og_mag_canvas(self):
        self.noise_removal_og_mag_figure = plt.figure()
        self.noise_removal_og_mag_figure.patch.set_facecolor('black')
        self.noise_removal_og_mag_plot = Canvas(self.noise_removal_og_mag_figure)
        self.noise_removal_og_mag_plot.mpl_connect('button_press_event', Display.on_press)
        self.noise_removal_og_mag_plot.mpl_connect('button_release_event', Display.on_release)
        self.noise_removal_og_mag_plot.mpl_connect('motion_notify_event', Display.on_motion)

        self.toolbar = NavigationToolbar(self.noise_removal_og_mag_plot, self)
        self.toolbar.setMaximumWidth(300)
        self.horizontalLayout_27.addWidget(self.toolbar)
        self.horizontalLayout_27.addWidget(self.noise_removal_apply)
        self.noise_removal_og_mag_box.addWidget(self.noise_removal_og_mag_plot)

    def create_noise_removal_after_canvas(self):
        self.noise_removal_after_figure = plt.figure()
        self.noise_removal_after_figure.patch.set_facecolor('black')
        self.noise_removal_after_plot = Canvas(self.noise_removal_after_figure)
        self.noise_removal_after_box.addWidget(self.noise_removal_after_plot)

    def create_noise_removal_after_mag_canvas(self):
        self.noise_removal_after_mag_figure = plt.figure()
        self.noise_removal_after_mag_figure.patch.set_facecolor('black')
        self.noise_removal_after_mag_plot = Canvas(self.noise_removal_after_mag_figure)
        self.noise_removal_after_mag_box.addWidget(self.noise_removal_after_mag_plot)




    def create_phantom_canvas(self):
        self.phantom_figure = plt.figure()
        self.phantom_figure.patch.set_facecolor('black')
        self.phantom_plot = Canvas(self.phantom_figure)
        self.phantom_box.addWidget(self.phantom_plot)

    def create_phantom_noise_canvas(self):
        self.phantom_noise_figure = plt.figure()
        self.phantom_noise_figure.patch.set_facecolor('black')
        self.phantom_noise_plot = Canvas(self.phantom_noise_figure)
        plt.axis('off')
        self.phantom_noise_plot.mpl_connect('button_press_event', self.noise_model.on_press)
        self.phantom_noise_plot.mpl_connect('button_release_event', self.noise_model.on_release)
        self.phantom_noise_plot.mpl_connect('motion_notify_event', self.noise_model.on_motion)
        self.phantom_noise_box.addWidget(self.phantom_noise_plot)

    def create_phantom_histo_canvas(self):
        self.phantom_histo_figure = plt.figure()
        self.phantom_histo_figure.patch.set_facecolor('black')
        self.phantom_histo_plot = Canvas(self.phantom_histo_figure)
        self.phantom_histo_box.addWidget(self.phantom_histo_plot)




    # Takes in a figure, makes it active and draws
    def display_image(self, figure, data):
        Display.clear_image(figure)
        plt.figure(figure.number)
        plt.axis('off')

        if figure == self.nn_figure or figure == self.bilinear_figure: plt.figimage(data, interpolation='None', cmap='gray')
        else: plt.imshow(data, interpolation='None', cmap='gray') # Autofits image in main plot

        plt.draw()

    def clear_image(figure):
        plt.figure(figure.number)
        plt.clf()
        plt.draw()

    def display_histo(figure, data, depth = 256):
        if depth < 256: depth = 256
        Display.clear_image(figure)
        plt.figure(figure.number)
        plt.bar(np.arange(depth), height=data)
        plt.draw()


    def display_metadata(self, dict):
        if self.metadata_layout.isEmpty() == False:
            Display.clear_layout(self)

        # CREATE QLABELS CONTAINING DICTIONARY ITEMS AND ADD THEM TO THE LAYOUT
        for key in dict:
            self.labl = QLabel(self)
            self.labl.setText(key + str(dict[key]))

            self.metadata_layout.addWidget(self.labl)

        # Show original size in 'Resize' tab
        self.original_label.setText(str(dict['Width: ']) + 'x' + str(dict['Height: ']) + ' \u2794 ')

    # CLEARS METADATA LAYOUT
    def clear_layout(self):
        while self.metadata_layout.count():
            child = self.metadata_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
