from modules.displays import Display
import matplotlib.pylab as plt
import numpy as np
from matplotlib.patches  import Rectangle
from modules.equalization import HistogramEqualizer

class NoiseModels:
    
    phantom_array = []
    noise_phantom_array = []

    # ROI coordinates
    roi_x0 = None
    roi_y0 = None
    roi_x1 = None
    roi_y1 = None
    
    is_pressed = False

    # ROI rectangle
    rect = None


    def create_phantom(self, mw):
        phantom_array = np.full((256,256), 50)
        
        # Create square in the middile
        phantom_array[31:224, 31:224] = 150

        # Create circle
        for x in range(len(phantom_array[0])):
            for y in range(len(phantom_array[1])):
                # Check if coordinate lies within circle using the equation of a circle
                if (x - 127) ** 2 + (y - 127) ** 2 <= 64 ** 2:
                    phantom_array[x][y] = 250

        self.phantom_array = phantom_array

        mw.generate_phantom_button.hide()
        mw.noise_options.show()            
        Display.display_image(mw, mw.phantom_figure, self.phantom_array)
        plt.axis('on')

    def add_noise(self, mw, arg1, arg2, noise_type):
        # Create gaussian OR uniform noise depending on input
        if noise_type == 'Gaussian':
            noise = np.random.normal(arg1, arg2, self.phantom_array.shape)
        elif noise_type == 'Uniform':
            noise = np.random.uniform(arg1, arg2, self.phantom_array.shape)

        # Round values
        self.noise_phantom_array = np.round(noise + self.phantom_array)
            
        Display.display_image(mw, mw.phantom_noise_figure, self.noise_phantom_array)
        plt.axis('on')

        # Prepare rectangular patch for roi selection
        self.rect = Rectangle((0,0), 0, 0)
        self.rect.set_color('r')
        self.rect.set_alpha(0.3)
        Display.mw.phantom_noise_figure.gca().add_patch(self.rect)


    '''
    Event functions passed to matplotlib on mouse press events
    '''
    def on_press(self, event):
        self.is_pressed = True
        self.roi_x0 = event.xdata
        self.roi_y0 = event.ydata
        self.rect.set_x(self.roi_x0)
        self.rect.set_y(self.roi_y0)

    def on_motion(self, event):
        if self.is_pressed == True:
            self.roi_x1 = event.xdata
            self.roi_y1 = event.ydata
            self.rect.set_width(self.roi_x1 - self.roi_x0)
            self.rect.set_height(self.roi_y1 - self.roi_y0)
            Display.mw.phantom_noise_plot.draw()

    def on_release(self, event):
        self.is_pressed = False

        # Rearrange initial and final coordinates of rectangle if needed to be able to slice array
        if self.roi_x0 > self.roi_x1:
            temp = self.roi_x0
            self.roi_x0 = self.roi_x1
            self.roi_x1 = temp
        if self.roi_y0 > self.roi_y1:
            temp = self.roi_y0
            self.roi_y0 = self.roi_y1
            self.roi_y1 = temp

        # Slice phantom array given the selected roi coordinates
        roi_array = self.noise_phantom_array[round(self.roi_y0):round(self.roi_y1), round(self.roi_x0):round(self.roi_x1)]

        # Calculate histogram array
        histo_array = HistogramEqualizer.calculate_histo_array(self, roi_array)

        # Calculate histogram mean
        mean = self.calculate_histo_mean(histo_array)

        # Calulate histogram sigma
        sigma = self.calculate_histo_sigma(histo_array, mean)

        Display.mw.mean_label.setText(str(mean))
        Display.mw.sigma_label.setText(str(sigma))
        Display.display_histo(Display.mw.phantom_histo_figure, histo_array, np.amax(roi_array) + 1)


    def calculate_histo_mean(self, histo):
        mean = 0
        for i in range(len(histo)):
            mean += i * histo[i]
        return round(mean, 5)

    def calculate_histo_sigma(self, histo, mean):
        var = 0
        for i in range(len(histo)):
            var += (i - mean) ** 2 * histo[i]

        return round(np.sqrt(var), 5)
