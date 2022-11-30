from PyQt5 import QtWidgets, uic
from modules import interface
from modules.displays import Display
import sys
import os
import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    ''' This is the PyQt5 GUI Main Window'''

    def __init__(self, *args, **kwargs):
        ''' Main window constructor'''

        cur_dir = os.path.dirname(__file__)
        cur_dir = cur_dir.removesuffix('\src')


        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(f'{cur_dir}/resources/MainWindow.ui', self)

        # set the title and icon
        # self.setWindowIcon(QtGui.QIcon('resources/icon.png'))
        self.setWindowTitle("Image Mixer")

        # initialize UI
        self.disp = Display(self)
        interface.init_connectors(self)



def main():

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
