import numpy as np
from modules.spatial_filtering import UnsharpMasking

class MorphologicalProcessing:

    def __init__(self, image):
        self.image = image
        self.accumulative_image = image
        self.accumulate = False

    def set_accumulative(self, value):
        self.accumulate = value

    def create_structural_element(self, x, y):
        st_element = np.ones((x, y), dtype=np.uint8)
        if x > 1:
            st_element[0][0] = 0
            st_element[0][y-1] = 0
        if y > 1:
            st_element[x-1][0] = 0
            st_element[x-1][y-1] = 0
        print(st_element)
        return st_element

    def erosion_dilation(self, image, st_elem, type):

        # Pad image
        padded_array = UnsharpMasking.pad_image(image, (st_elem.shape[0], st_elem.shape[1]))
        
        # Initialize output array
        output_array = np.zeros(image.shape)

        # Offsets of start and end of structural element traversal with respect to padded image
        offset_x = st_elem.shape[0] // 2
        offset_y = st_elem.shape[1] // 2
        rows_stop = image.shape[0] + offset_x
        col_stop = image.shape[1] + offset_y

        # Loop over image and check whether structural element is fully contained within a shape's borders
        for x in range(offset_x, rows_stop):
            for y in range(offset_y, col_stop):
                # Aree of image under structural element
                st_elem_area = padded_array[x-offset_x:x+offset_x+1, y-offset_y:y+offset_y+1]

                # Check if structural element fits/hits
                output_array[x-offset_x][y-offset_y] = self.process_st_elem_presence(st_elem_area, st_elem, type)

        return output_array


    def process_st_elem_presence(self, arr, st_elem, type):
        # Flatten arrays
        arr = arr.flatten()
        st_elem = st_elem.flatten()

        # Loop over arrays and check if st_elem fits/hits
        for i in range(len(st_elem)):
            if type == 'Erosion':       # Check is and pixel does not fit
                if st_elem[i] == 1 and arr[i] == 0: return 0
            elif type == 'Dilation':    # Check if any pixel hits
                if st_elem[i] == 1 and arr[i] == 1: return 1

        if type == 'Erosion': return 1      # All pixels fit
        elif type == 'Dilation': return 0   # No pixel hits


    def opening_closing(self, image, st_elem, type):
        # Apply erosion followed by dilation
        if type == 'Opening':
            morphed = self.erosion_dilation(image, st_elem, 'Erosion')
            morphed = self.erosion_dilation(morphed, st_elem, 'Dilation')
        # Apply dilation followed by erosion
        elif type == 'Closing':
            morphed = self.erosion_dilation(image, st_elem, 'Dilation')
            morphed = self.erosion_dilation(morphed, st_elem, 'Erosion')

        return morphed


    def apply_morph_operation(self, x, y, type):
        # Whether to apply on accumulated image or original
        if self.accumulate: image = self.accumulative_image
        else: image = self.image

        # Create structural element from user input
        st_elem = self.create_structural_element(x, y)

        # Apply morphological operation
        if type == 'Erosion' or type == 'Dilation':
            morphed = self.erosion_dilation(image, st_elem, type)
        elif type == 'Opening' or type == 'Closing':
            morphed = self.opening_closing(image,st_elem, type)
        elif type == 'Noise Removal':
            morphed = self.remove_fingerprint_noise()

        self.accumulative_image = morphed

        return morphed


    


    
    def remove_fingerprint_noise(self):
        st_elem = self.create_structural_element(3, 3)
        opened = self.opening_closing(self.image, st_elem, 'Opening')
        closed = self.opening_closing(opened, st_elem, 'Closing')
        return closed