#!/usr/bin/env python3
import time, datetime
import sys
import os
import argparse
import logging

from PIL import Image, ImageDraw, ImageFont
from traceback import format_exception

sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/rpi-rgb-led-matrix/bindings/python")
from sun_times import SunDisplayer

# region --- initialise logging ---
# logger = logging.getLogger(__name__)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)
# fh = logging.FileHandler(f'{os.path.dirname(os.path.realpath(__file__))}/mta-board.log')
# fh.setLevel(logging.DEBUG)
# logger.addHandler(fh)

# def handle_exception(exc_type, exc_value, exc_traceback):
#     if issubclass(exc_type, KeyboardInterrupt):
#         sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         return

#     logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# sys.excepthook = handle_exception
# endregion

class MatrixBoard():
    def __init__(self, debug:bool=False, emulate:bool=False, *args, **kwargs):
        self.debug: bool = debug
        if emulate: from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
        else: from rgbmatrix import RGBMatrix, RGBMatrixOptions
        self.logger: logging.Logger = logging.getLogger()
        if self.debug: self.logger.setLevel(logging.DEBUG)
        else: self.logger.setLevel(logging.WARNING)

        # Configuration for the matrix
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.brightness = 60
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
        options.led_rgb_sequence = "RBG"
        options.gpio_slowdown = 3
        # options.pwm_lsb_nanoseconds = 130
        options.limit_refresh_rate_hz = 160
        options.show_refresh_rate = 0

        self.dir = os.path.dirname(os.path.realpath(__file__)) # directory of this file
        # self.logo = Image.open(f'{self.dir}/assets/images/L_logo.png').convert('RGBA') # pull logo from the assets

        self.matrix = RGBMatrix(options = options) # init the matrix with its options

        self.running = False # start as not running
        self.startTime: float = 0

    def run(self):
        self.displayer = SunDisplayer(34.110856, -118.272459)
        self.lastTodayUpdate: float = time.time()

        self.canvas = self.matrix.CreateFrameCanvas()

        self.running = True # start things up
        self.startTime = time.time()

        while self.running:
            self.image = Image.new('RGBA', (self.matrix.width, self.matrix.height)) # new PIL image to build on
            # -- reload current time every 10 seconds --
            if time.time() - self.lastTodayUpdate > 10:
                self.displayer.today = datetime.datetime.today()
                self.lastTodayUpdate = time.time()
            # -- reload sunData when the day changes --
            if self.displayer.todayData.date.day != self.displayer.today.day:
                self.displayer.reloadData()
            self.displayer.showSun = False if int(time.time()*1.5) % 2 == 0 else True

            sunImage = self.displayer.generateImage()
            self.image.paste(sunImage, (0,0))


            self.canvas.Clear() # clear whatever's on the screen
            self.canvas.SetImage(self.image.convert('RGB'), 0, 0) # transfer the PIL image to the canvas

            time.sleep(0.005) # the nominal fastest tick time
            self.canvas = self.matrix.SwapOnVSync(self.canvas) # pulls in the just-generated canvas on the next frame

            if time.time() - self.startTime > 3600: self.running = False # self-destruct hour

    # def showIP(self):
    #     """
    #     Show the machine's wifi IP on the screen
    #     """
    #     ip: str = subprocess.check_output(['ipconfig getifaddr en0'], encoding='UTF-8')
    #     ipBox = TextBox(text=ip, font=self.font, x=0, y=-1)
    #     ipBox.addToImage(self.image, (1,1))

# class TextBox:
#     """
#     Represents a text box that can be added to the board.
#     self.outputImage and self.addToImage are the best ways to get the text

#     Parameters:
#         text (str): the text to show
#         font (ImageFont.FreeTypeFont): your font of choice
#         x (int): shift the font within the text box in x. Defaults to 0
#         y (int): shift the font within the text box in y. Defaults to 0
#         width (int): Optional argument to force the box width (good for scrolling text)
#         height (int): Optional argument to force the box height (good for weird fonts)
#         type (str): can be 'static', 'scrolling', or 'blinking'
#         i (int): link this to something that ticks at the fequency you want animations to update at
#     """
#     def __init__(self,
#                  text:str,
#                  font:ImageFont.FreeTypeFont,
#                  fill:str|None = None,
#                  x:int=None,
#                  y:int=None,
#                  width:int=None,
#                  height:int=None,
#                  type:str='static',
#                  i:int=0,
#                  ):

#         self.text = str(text)
#         self.font = font
#         self.type = type
#         self.fill = fill
#         self.i = i
#         self.holdSteps = 40 # ticks to hold between scrolling

#         boundingBox = self.font.getmask(self.text).getbbox()
#         self.textWidth = boundingBox[2]
#         self.textHeight = boundingBox[3]
#         self.width = width if width else self.textWidth # default to the calculated width if no arg given
#         self.height = height if height else self.textHeight # default to the calculated height if no arg given

#         self.x = x if x else 0 # default to the zero offset if no arg given
#         self.y = y if y else 0 # default to the zero offset if no arg given

#         match font.font.family: # some defaults for fonts I know the offsets of
#             case '04b03':
#                 self.y = y if y else -1 # default to the -1 offset if no arg given

#         self.outputImage = Image.new('RGBA', (self.width, self.height)) # blank image to draw on
#         self.outputDraw = ImageDraw.Draw(self.outputImage) # draw object to use for adding text

#         match self.type:
#             case 'scrolling':
#                 self.showScrollingText()
#             case 'blinking':
#                 if int(self.i)%2: # show text every other tick
#                     self.showStaticText()
#             case _:
#                 self.showStaticText()

#     def showStaticText(self):
#         self.outputDraw.text((self.x, self.y), self.text, fill=self.fill, font=self.font)

#     def showScrollingText(self):
#         spacing = int(self.textHeight * 2) # this is a nice amount of spacing. I'm hardcoding it!
#         scrollWidth = self.textWidth + spacing # width of the scrolling element with its spacing

#         if self.textWidth < self.width: # if there's no point in scrolling because the whole text fits
#             self.showStaticText() # just show the text
#             return None

#         positions = [-2*scrollWidth, -scrollWidth, 0] # create some instances that can scroll into the screen
#         posAdjustment = self.i % (scrollWidth + self.holdSteps) # the amount to scoot each instance over by each time
#         # the line above does a modulo of the scrollwidth because restarting after that many steps is seamless.
#         # holdSteps just makes the scrolling hesitate so it's easier to read

#         for pos in positions: # for each instance of the text
#             if posAdjustment <= scrollWidth: # only shift the text for one unit of scrolling
#                 pos += posAdjustment # shift text to the right
#             self.outputDraw.text((pos, self.y), self.text, fill=self.fill, font=self.font)

#     def addToImage(self, imgObj:ImageDraw.ImageDraw, pos:tuple[int, int]):
#         imgObj.paste(im=self.outputImage, box=pos) # plop the textbox image into the parent image at the given position


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action="store_true", required=False)
    parser.add_argument('-e', '--emulate', action="store_true", required=False)
    args = parser.parse_args()

    try:
        board = MatrixBoard(debug=args.debug, emulate=args.emulate)
        board.run()
        del board
    except Exception as ex:
        if args.debug:
            raise ex
        else:
            logging.error(''.join(format_exception(None, ex, ex.__traceback__)))