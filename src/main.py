from PyQt5 import QtGui, QtWidgets, uic
from modules import interface
from modules.displays import Display
from modules.size_interpolation import Interpolate
import sys


class MainWindow(QtWidgets.QMainWindow):
    ''' This is the PyQt5 GUI Main Window'''

    def __init__(self, *args, **kwargs):
        ''' Main window constructor'''

        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('F:/zeyad/Documents/repos/GitHub/DICOM-Viewer/resources/MainWindow.ui', self)

        # set the title and icon
        self.setWindowIcon(QtGui.QIcon('F:/zeyad/Documents/repos/GitHub/DICOM-Viewer/resources/icon.png'))
        self.setWindowTitle("Image Mixer")

        # initialize UI
        Display.create_main_canvas(self)
        Display.create_neaarest_neighbor_canvas(self)
        Display.create_bilinear_canvas(self)
        # interface.create_plots_canvas(self)
        interface.init_connectors(self)
        # Interpolate.interpolate_nearest_neighbor()



def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
