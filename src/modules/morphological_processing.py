import numpy as np

class MorphologicalProcessing:

    def __init__(self, image):
        self.image = image
        self.accumulative_image = image
        self.accumulate = False

    def set_accumulative(self, value):
        self.accumulate = value

    def create_structural_element(self, x, y):
        st_element = np.ones((x, y), dtype=np.uint8)
        return st_element

    def erosion_dilation(self, image, st_elem, type):
        
        # Initialize output array
        output_array = np.zeros(image.shape)

        # Offsets of start and end of structural element traversal with respect to image
        offset_x = st_elem.shape[0] // 2
        offset_y = st_elem.shape[1] // 2
        rows_stop = image.shape[0] - offset_x
        col_stop = image.shape[1] - offset_y

        # Loop over image and check whether structural element us fully contained within a shape's borders
        for x in range(offset_x, rows_stop):
            for y in range(offset_y, col_stop):
                # Aree of image under structural element
                st_elem_area = image[x-offset_x:x+offset_x+1, y-offset_y:y+offset_y+1]
                # Multiply structural element (all 1s) with corresponding pixels
                product = st_elem_area * st_elem

                if type == 'Erosion': output_array[x][y] = np.min(product)      # pixel replaced with 0 if product returned any 0s
                elif type == 'Dilation': output_array[x][y] = np.max(product)   # pixel replaced with 1 is product returned any 1s

        return output_array


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

        self.accumulative_image = morphed

        return morphed


    


    
    def remove_fingerprint_noise(self):
        st_elem = self.create_structural_element(3, 3)
        opened = self.opening_closing(self.image, st_elem, 'Opening')
        closed = self.opening_closing(opened, st_elem, 'Closing')
        return closed