import numpy as np
from modules.spatial_filtering import UnsharpMasking

class MorphologicalProcessing:

    def __init__(self, image):
        self.image = image

    def create_structural_element(x, y):
        st_element = np.ones((x, y), dtype=np.uint8)
        return st_element

    def erode_image(image, st_elem):
        
        padded_image = UnsharpMasking.pad_image(image, (st_elem.shape[0], st_elem.shape[1]))

        # Initialize output array
        output_array = np.zeros(image.shape)

        # Offsets of start and end of original image with respect to padded image
        offset_x = st_elem.shape[0] // 2
        offset_y = st_elem.shape[1] // 2
        rows_stop = offset_x + image.shape[0]
        col_stop = offset_y + image.shape[1]

        # # Loop over padded image and calculate output of box filter at each pixel
        # for x in range(offset_x, rows_stop):
        #     for y in range(offset_y, col_stop):
        #         mask = padded_array[x-offset:x+offset+1, y-offset:y+offset+1]       # This is the local sub-image that lies under the kernel
        #         output_array[x-offset][y-offset] = round(self.matrix_sum(box_kernel, mask) / (size ** 2))