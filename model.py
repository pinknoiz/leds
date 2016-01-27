import json
from connection import pixels, draw
import operator
from color import set_brightness_multiplier

class Model(object):

    def __init__(self, model_file):
        self.model = None
        self.load_model(model_file)

        self.shaders = []            # list of shader functions to be called
        self._brightness = 1.0

    def register_shader(self,shader):
        self.shaders.append(shader)

    def reset_shaders(self):
        self.shaders = []

    def get_shaders(self):
        return self.shaders

    def map_pixels(self):
        # set all pixels by mapping each element of the "model" through 
        # "fn" and setting the corresponding pixel value. The "fn" function 
        # returns a tuple of three 8-bit RGB values.
    
        # print "active shaders: %s" % self.shaders
        
        for i, led in enumerate(self.model):
            # first one sets the base, others are 'add'-ed in
            pixels[i] = self.shaders[0](led)
            for shader in self.shaders[1:]:
                values = shader(led) 
                pixels[i] = tuple(map(operator.add, pixels[i], values))
            if self._brightness != 1.0:
                # adjust brightness
                pixels[i] = set_brightness_multiplier(pixels[i], self._brightness)
        draw()

    def set_brightness(self, val):
        self._brightness = val

    def clear(self):
        black = (0,0,0)

        for i, led in enumerate(pixels):
            pixels[i] = black
       
        # draw()        # -- this will be called implicitly

    def load_model(self, filename):

        with open(filename) as data_file:    
            data = json.load(data_file)
        print "Loading model: %s" % filename

        self.model = data

    def set_pixel(self, pixel, color):
        if self._brightness != 1.0:
            pixels[pixel] = set_brightness_multiplier(color, self._brightness)
        else:
            pixels[pixel] = color
    
    def draw(self):
        draw()      

    def get_nof_pixels(self):
        return len(pixels)
