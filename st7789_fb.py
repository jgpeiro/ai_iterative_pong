from machine import Pin, SPI
import framebuf
import time

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD( framebuf.FrameBuffer ):
    def width( self ):
        return 240
    def height( self ):
        return 135
    def pixel( self, x, y, c=None ):
        if( c is None ):
            return super().pixel( int(x), int(y) )
        else:
            super().pixel( int(x), int(y), int(c) )
    def rect( self, x, y, w, h, c ):
        super().rect( int(x), int(y), int(w), int(h), int(c) )
    def rectangle( self, x, y, w, h, c ):
        super().rect( int(x), int(y), int(w), int(h), int(c) )
    def fill_rect( self, x, y, w, h, c ):
        super().fill_rect( int(x), int(y), int(w), int(h), int(c) )
    def fill_rectangle( self, x, y, w, h, c ):
        super().fill_rect( int(x), int(y), int(w), int(h), int(c) )
    def line( self, x0, y0, x1, y1, c ):
        super().line( int(x0), int(y0), int(x1), int(y1), int(c) )
    def text( self, txt, x, y, c ):
        super().text( txt, int(x), int(y), int(c) )
    
    def __init__(self):
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height() * self.width() * 2)
        super().__init__(self.buffer, self.width(), self.height(), framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.yellow=   0xffe0
        self.cyan  =   0x07ff
        self.magenta=  0xf81f
        self.gray  =   0x8410
        self.darkgray= 0x4208
        self.lightgray=0xC618
    def circle( self, x, y, r, c ):
        self.__circle( int(x), int(y), int(r), c, False )
    def fill_circle( self, x, y, r, c ):
        self.__circle( int(x), int(y), int(r), c, True )
        self.line( x - r, y - 1, x + r, y - 1, c )
        self.line( x - r, y + 1, x + r, y + 1, c )
        self.line( x - r, y - 0, x + r, y - 0, c )
    
    def __circle( self, x, y, r, c, fill ):
        # Bresenham’s circle drawing algorithm
        x0, y0 = x, y
        f = 1 - r
        ddf_x = 1
        ddf_y = -2 * r
        x = 0
        y = r
        self.pixel( x0, y0 + r, c )
        self.pixel( x0, y0 - r, c )
        self.pixel( x0 + r, y0, c )
        self.pixel( x0 - r, y0, c )
        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            if fill:
                self.line( x0 - x, y0 + y, x0 + x, y0 + y, c )
                self.line( x0 - x, y0 - y, x0 + x, y0 - y, c )
                self.line( x0 - y, y0 + x, x0 + y, y0 + x, c )
                self.line( x0 - y, y0 - x, x0 + y, y0 - x, c )
            else:
                self.pixel( x0 + x, y0 + y, c )
                self.pixel( x0 - x, y0 + y, c )
                self.pixel( x0 + x, y0 - y, c )
                self.pixel( x0 - x, y0 - y, c )
                self.pixel( x0 + y, y0 + x, c )
                self.pixel( x0 - y, y0 + x, c )
                self.pixel( x0 + y, y0 - x, c )
                self.pixel( x0 - y, y0 - x, c )
    
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
