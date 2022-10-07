from PyQt5.QtWidgets import QFileDialog
from modules import interface
from modules import image_data

def browse_window(self):

    self.filename = QFileDialog.getOpenFileName(
        None, 'open the image file', './', filter="Raw Data(*.bmp *.jpg *.png *.dcm)")

    path = self.filename[0]

    if path != '':

        data = image_data.ImageData(path)
        
        try:
            interface.display_image(self, data.plot_data)
            interface.display_metadata(self, data.get_attributes())
        except: interface.clear_plot(self)