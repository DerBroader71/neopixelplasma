"""
    Multicolored Plasma for the Arduino Micro-Controller and NeoPixel Shield
    Copyright (C) 2019 John Ericksen
    Multicolored Plasma for CircuitPython/CPython and NeoPixel Shield
    Copyright (C) 2022 Tudor Davies
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.
"""
import board
import math
from adafruit_seesaw import seesaw, neopixel

# setup Seesaw I2C device
ss = seesaw.Seesaw(board.I2C(), 0x49)

# setup neopixel
pixel_pin = 0  # neopixel Shield is connected to Pin 0 on the Seesaw board
ROWS = 5
COLS = 8
pixel_num = ROWS * COLS
pixels = neopixel.NeoPixel(ss, pixel_pin, pixel_num, brightness=0.1, auto_write=False, pixel_order=(1, 0, 2, 3))

# blank the neopixel shield
pixels.fill((0, 0, 0, 0))
pixels.show()

# define some variables and dicts
phaseIncrement = float(0.08)  # Controls the speed of the moving points. Higher == faster. I like 0.08 . was 0.03
colorStretch = float(0.11)    # Higher numbers will produce tighter color bands. I like 0.11 . was 0.3
phase = float(0.0)
Point = {}
Point['p1'] = {}
Point['p2'] = {}
Point['p3'] = {}
Point['dist1'] = {}
Point['dist2'] = {}
Point['dist3'] = {}


# function to ensure the interger passed is limited
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


while True:
    phase += phaseIncrement
    Point['p1']['x'] = (math.sin(phase*1.000)+1.0) * 4.5
    Point['p2']['x'] = (math.sin(phase*1.770)+1.0) * 4.5
    Point['p3']['x'] = (math.sin(phase*0.250)+1.0) * 4.5

    Point['p1']['y'] = (math.sin(phase*1.310)+1.0) * 4.0
    Point['p2']['y'] = (math.sin(phase*2.865)+1.0) * 4.0
    Point['p3']['y'] = (math.sin(phase*0.750)+1.0) * 4.0

    for row in range(ROWS):
        row_f = float(row)  # Optimization: Keep a floating point value of the row number, instead of recasting it repeatedly.

        # For each column...
        for col in range(COLS):
            col_f = float(col)  # Optimization.

            # Calculate the distance between this LED, and p1.
            Point['dist1']['x'] = col_f - Point['p1']['x']
            Point['dist1']['y'] = row_f - Point['p1']['y']  # The vector from p1 to this LED.
            distance1 = math.sqrt(Point['dist1']['x']*Point['dist1']['x'] + Point['dist1']['y']*Point['dist1']['y'])

            # Calculate the distance between this LED, and p2.
            Point['dist2']['x'] = col_f - Point['p2']['x']
            Point['dist2']['y'] = row_f - Point['p2']['y']  # The vector from p2 to this LED.
            distance2 = math.sqrt(Point['dist2']['x']*Point['dist2']['x'] + Point['dist2']['y']*Point['dist2']['y'])

            # Calculate the distance between this LED, and p3.
            Point['dist3']['x'] = col_f - Point['p3']['x']
            Point['dist3']['y'] = row_f - Point['p3']['y']  # The vector from p3 to this LED.
            distance3 = math.sqrt(Point['dist3']['x']*Point['dist3']['x'] + Point['dist3']['y']*Point['dist3']['y'])

            # Warp the distance with a sin() function. As the distance value increases, the LEDs will get light,dark,light,dark,etc...
            # You can use a cos() for slightly different shading, or experiment with other functions. Go crazy!
            color_1 = distance1  # range: 0.0...1.0
            color_2 = distance2
            color_3 = distance3
            color_4 = (math.sin(distance1 * distance2 * colorStretch)) + 2.0 * 0.5

            # Square the color_f value to weight it towards 0. The image will be darker and have higher contrast.
            color_1 *= color_1 * color_4
            color_2 *= color_2 * color_4
            color_3 *= color_3 * color_4
            color_4 *= color_4

            # Scale the color up to 0..7 . Max brightness is 7.
            # print(clamp(int(color_1), 0, 255), clamp(int(color_2), 0, 255), clamp(int(color_3), 0, 255))
            pixels[col + (COLS * row)] = (clamp(int(color_1), 0, 255), clamp(int(color_2), 0, 255), clamp(int(color_3), 0, 255), 0)

    pixels.show()
