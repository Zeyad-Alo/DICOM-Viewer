from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLabel
from modules import openfile
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pylab as plt


def display_image(self, data):
    '''
    Display the image data in a QPixmap given a key to the display_reference_dict
    '''

    plt.imshow(data, cmap='gray')
    self.image_plot.draw()
    self.figure.canvas.draw()
    return



def display_metadata(self, dict):

    if self.verticalLayout_6.isEmpty() == False:
        clear_layout(self.verticalLayout_6)

    for key in dict:
        self.labl = QLabel(self)
        self.labl.setText(key + str(dict[key]))

        self.verticalLayout_6.addWidget(self.labl)


# CLEARS METADATA LAYOUT
def clear_layout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().deleteLater()


# CREATES MATPLOTLIB FIGURE
def init_plot(self):
    self.figure = plt.figure()
    self.figure.patch.set_facecolor('black')
    self.axes = self.figure.add_subplot()
    self.image_plot = Canvas(self.figure)
    self.verticalLayout_5.addWidget(self.image_plot)


def init_connectors(self):
    '''Initializes all event connectors and triggers'''

    ''' Browse buttons'''
    # self.metadata_groupBox.hide()

    self.insert_image_pushButton.clicked.connect(
        lambda: openfile.browse_window(self))