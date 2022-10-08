from PIL import Image
from PyQt5.QtWidgets import QMessageBox
import os
import pydicom as dicom

class ImageData:
    # DICTIONARY FOR BIT DEPTHS ACCORDING TO MODE
    mode_to_depth = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    plot_data = []

    def __init__(self, path):
        self.path = path

        # GET EXTENSION
        extension = os.path.splitext(path)[1]

        if extension == '.dcm':
            self.import_dicom()
        else:
            self.import_general()


    # READ AS DICOM AND CONFIGURE ATTRIBUTES
    def import_dicom(self):

        # CHECK FILE HEALTH
        try: ds = dicom.dcmread(self.path)
        except:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("DICOM Exception")
            error.setInformativeText('File is corrupted or missing DICOM header.')
            error.setWindowTitle("Error")
            error.exec_()
            return

        self.plot_data = ds.pixel_array

        # CONFIG METADATA
        self.format = 'DICOM'
        try: self.width = ds.Columns 
        except AttributeError: self.width = ''
        try: self.height = ds.Rows
        except AttributeError: self.height = ''
        self.size = os.stat(self.path).st_size
        try: self.depth = ds.BitsAllocated
        except AttributeError: self.depth = ''
        try: self.colorMode = ds.PhotometricInterpretation
        except AttributeError: self.colorMode = ''

        try: self.modality = ds.Modality
        except AttributeError: self.modality = ''
        try: self.patientName = ds.PatientName
        except AttributeError: self.patientName = ''
        try: self.patientAge = ds.PatientAge
        except AttributeError: self.patientAge = ''
        try: self.bodyPartExaminded = ds.StudyDescription
        except AttributeError: self.bodyPartExaminded = ''


    # READ AS NORMAL IMAGE AND CONFIGURE ATTRIBUTES
    def import_general(self):
        image = Image.open(self.path)
        self.plot_data = image

        self.format = image.format
        self.width = image.width
        self.height = image.height
        self.size = os.stat(self.path).st_size
        self.colorMode = image.mode
        self.depth = self.mode_to_depth[self.colorMode]


    def get_attributes(self):

        # LIST COMMON ATTRIBUTES IN A DICT
        dict = {
            'Format: ': self.format,
            'Width: ': self.width,
            'Height: ': self.height,
            'Size: ': self.size,
            'Color Mode: ': self.colorMode,
            'Bit Depth: ': self.depth
        }

        # ADD EXTRA DICOM ATTRIBUTES AND UPDATES DICT
        if self.format == 'DICOM':
            dicom_extra = {
                'Modality: ': self.modality,
                'Patient Name: ': self.patientName,
                'Patient Age: ': self.patientAge,
                'Examination Description: ': self.bodyPartExaminded,
            }

            dict.update(dicom_extra)


        return dict