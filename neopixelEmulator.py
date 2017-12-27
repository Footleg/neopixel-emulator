#!/usr/bin/env python3
import pygame, math, time

def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue

class mock():
    WS2811_STRIP_RGB = 1
    WS2811_STRIP_GRB = 2


ws = mock()

class Neopixel_Emulator(object):
    """ A Pygame based application class to emulate an array of neopixels.
        The interface is based on the Adafruit Neopixel library python class
        so your code written against the emulator should work with that library
        and real neopixel devices without changes.

    """
        
    
    def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False,
                brightness=255, channel=0, strip_type=ws.WS2811_STRIP_RGB):
        """Class to represent a NeoPixel/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 5), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """
        
        #Store parameters
        self.brightness = brightness
        self._numLEDs = num
        
        #Set initial values
        self._initialised = False
        self._led_pos = []
        self._led_data = []
        self._height = 640
        self._width = 640
        
        #Create initial LED array data structure
        for i in range(0,num):
            self._led_pos.append( [0,0] )
            self._led_data.append( [0,0,0,0] )
        
        #Initialise pygame
        pygame.init()

        # Set the width and height of the screen [width,height]
        size = [self._width, self._height]
        self.screen = pygame.display.set_mode(size)

        pygame.display.set_caption("Footleg's Neopixel Enumulator")

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
    
        self.initialiseLEDCircle(num)
        
    
    def initialiseLEDCircle(self, num):
        """ Set LED positions in a circle """
        self._LEDsize = int( 20 / num ) + 10
        radius = int( num * 10 )
        
        #Position LEDs in a circle
        for i in range(0,num):
            angleRad = math.pi - (i * 2 * math.pi / num)
            x = int( radius * math.sin( angleRad ) + self._width / 2 )
            y = int( radius * math.cos( angleRad ) + self._height / 2 )
            self._led_pos[i] = [x,y]
        
        
    def begin(self):
        """ Initialize library, must be called once before other functions are
            called.
        """
        self._initialised = True
        

    def show(self):
        """ Update the display with the data from the LED buffer. """
        if self._initialised :
            #Redraw all the neopixels
            num = self.numPixels()
            for i in range( 0, num ):
                #Draw LED outline if completely off
                colour = self._led_data[i]
                if (colour[0] == 0) and (colour[1] == 0) and (colour[2] == 0):
                    pygame.draw.circle(self.screen, ([16,16,16]), self._led_pos[i], self._LEDsize )
                    pygame.draw.circle(self.screen, ([0,0,0]), self._led_pos[i], self._LEDsize - 2 )
                else:
                    pygame.draw.circle(self.screen, colour, self._led_pos[i], self._LEDsize)
            
            # Update the screen 
            pygame.display.flip()
        else:
            #Throw error as begin method of class has not been called
            print("Error: Class begin method was not called")
        
        
    def setPixelColor(self, n, color):
        """ Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        self._led_data[n] = color


    def setPixelColorRGB(self, n, red, green, blue, white = 0):
        """ Set LED at position n to the provided red, green, and blue color.
            Each color component should be a value from 0 to 255 (where 0 is the
            lowest intensity and 255 is the highest intensity).
        """
        self.setPixelColor(n, Color(red, green, blue, white))


    def setBrightness(self, brightness):
        """ Scale each LED in the buffer by the provided brightness.  A brightness
            of 0 is the darkest and 255 is the brightest.
        """


    def getPixels(self):
        """ Return an object which allows access to the LED display data as if 
            it were a sequence of 24-bit RGB values.
        """
        return self._led_data
    

    def numPixels(self):
        """ Return the number of pixels in the display."""
        return self._numLEDs


    def getPixelColor(self, n):
        """ Get the 24-bit RGB color value for the LED at position n."""
        return self._led_data[n]


def main():
    
    # LED strip configuration:
    LED_COUNT      = 24      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering
    
    # Create NeoPixel object with appropriate configuration.
    strip = Neopixel_Emulator(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    #In the emulator we need to check for the pygame QUIT event to exit our main program loop and shut down pygame.
    #This will enable to emulator program to exit when the user closes the window.
    keepRunning = True
    i = 0
    c = 0
    cmax = 2 * strip.numPixels()
    mode = 0
    
    while keepRunning == True :
        #Code to animate neopixels goes here
        
        #Set colour
        c1 = int( 255 * c / cmax )
        c2 = 0 
        c3 = 255 - c1
        if mode == 0:
            r = c3
            b = c2
            g = c1
        elif mode == 1:
            r = c2
            b = c1
            g = c3
        elif mode == 2:
            r = c1
            b = c3
            g = c2
            
        strip.setPixelColor(i,[r,g,b])
        strip.show()
        time.sleep(0.1)
        
        i = i + 1
        if i >= strip.numPixels():
            i = 0

        c = c + 1
        if c >= cmax:
            c = 0
            mode = mode + 1
            
        if mode > 2:
            mode = 0
            
        #Check for quit event (when user closes pygame window)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                keepRunning = False # Flag that we are done so we exit this loop
        
    pygame.quit()


if __name__ == '__main__':
    main()
