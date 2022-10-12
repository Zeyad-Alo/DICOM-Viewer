from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel
from modules import openfile
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pylab as plt


def display_image(self, data):

    plt.imshow(data, cmap='gray')
    self.image_plot.draw()
    self.figure.canvas.draw()
    return



def display_metadata(self, dict):

    if self.metadata_layout.isEmpty() == False:
        clear_layout(self)


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

def clear_image(self):
    self.axes.clear()
    self.image_plot.draw()
    self.figure.canvas.draw()


# CREATES MATPLOTLIB FIGURE
def init_plot(self):
    self.figure = plt.figure()
    self.figure.patch.set_facecolor('black')
    self.axes = self.figure.add_subplot()
    self.image_plot = Canvas(self.figure)
    self.image_box.addWidget(self.image_plot)


def init_connectors(self):
    self.insert_image_pushButton.clicked.connect(
        lambda: openfile.browse_window(self))