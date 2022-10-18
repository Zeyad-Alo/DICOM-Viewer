
from turtle import clear
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel
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
        self.nn_figure = plt.figure()
        self.nn_figure.patch.set_facecolor('black')
        self.nn_plot = Canvas(self.nn_figure)
        self.nearest_neighbor_box.addWidget(self.nn_plot)

    def create_bilinear_canvas(self):
        self.bilinear_figure = plt.figure()
        self.bilinear_figure.patch.set_facecolor('black')
        self.bilinear_plot = Canvas(self.bilinear_figure)
        self.bilinear_box.addWidget(self.bilinear_plot)

        
        

    # Takes in a figure, makes it active and draws
    def display_image(self, figure, data):
        Display.clear_image(self, figure)
        plt.figure(figure.number)
        if figure == self.main_figure: plt.imshow(data, cmap='gray')
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

    # CLEARS METADATA LAYOUT
    def clear_layout(self):
        while self.metadata_layout.count():
            child = self.metadata_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
