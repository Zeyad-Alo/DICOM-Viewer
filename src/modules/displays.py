
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pylab as plt

class Display:

    # CREATE BASE MATPLOTLIB CANVASES - CALLED ONCE ON LAUNCH

    def create_main_canvas(self):
        self.main_figure = plt.figure()
        self.main_figure.patch.set_facecolor('black')
        self.main_plot = Canvas(self.main_figure)
        self.image_box.addWidget(self.main_plot)

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

        
        

    # Takes in a figure, makes it active and draws
    def display_image(self, figure, data):
        Display.clear_image(self, figure)
        plt.figure(figure.number)

        if figure == self.main_figure: plt.imshow(data, cmap='gray') # Autofits image in main plot
        else: plt.figimage(data, cmap='gray')

        plt.draw()

    def clear_image(self, figure):
        plt.figure(figure.number)
        plt.clf()
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
