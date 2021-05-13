#!/usr/bin/env python3
# Michael Leahy, May 8, 2021

"""
"""

import logging
import unittest
import sys  # system calls
# import requests  # web requests
import re  # regular expressions
# import shutil  # shell utilities
import os  # OS utilities
import argparse
# from datetime import datetime
# from functools import reduce
# from operator import mul

try:
    from PIL import Image, ImageOps
except:
    print('This program requires the Pillow library:')
    print('  pip install Pillow')
    sys.exit(1)

# import bs4  # parse HTML (beautiful soup)

import timer

logging.basicConfig(
            level=logging.DEBUG,
            format=' %(asctime)s - %(levelname)s - %(message)s')

default_bg_transparency = 40 # percent


def command_line_args() -> argparse:
    parser = argparse.ArgumentParser(
                description="Invert an image and add a black background "
                            "that has TRANSPARENCY% of transparency")
    parser.add_argument("filename",
                        help="path to image file")
    parser.add_argument("-t", "--transparency",
                        type=int,
                        choices=range(0,101,10),
                        default=default_bg_transparency,
                        help="transparency of background")
    parser.add_argument("-s", "--show",
                        help="display image",
                        action='store_true')
    parser.add_argument("-o", "--outfile",
                        help="output file name")
    parser.add_argument("-c", "--color",
                        help="background color;"
                             " option 1: 0-255;"
                             " option 2: rrggbb (3 pairs of 2 hex digits);"
                             " option 3: '(rr,gg,bb)' (3 pairs of 2 ints, 0-255)",
                        default="0")
    return(parser.parse_args())


# https://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging

def invert(image: Image) -> Image:
    if image.mode == 'RGBA':
        r,g,b,a = image.split()
        rgb_image = Image.merge('RGB', (r,g,b))

        inverted_rgb = ImageOps.invert(rgb_image)

        r2,g2,b2 = inverted_rgb.split()

        inverted_image = Image.merge('RGBA', (r2,g2,b2,a))

    else:
        inverted_image = ImageOps.invert(image)

    return(inverted_image)


# Acceptable values for col
#    col = "0"-"255" (string versions of integer values 0:255)
#    col = "aabbcc"  (3 of 2 hex characters)
#    col = "(aa,bb,cc)"  (tuple of three integers, 0:255)
def parse_colors(col: str):
    colors = 0
    if col.isdigit() and len(col) <= 3:
        colors = int(col)
        colors = max(0, min(255, colors))
    elif len(col) == 6:
        # Check for invalid characters
        badhex = [col[ch].lower() for ch in range(0,len(col))
                     if col[ch].lower() not in "0 1 2 3 4 5 6 7 8 9 a b c d e f".split()]
        if badhex == []:
            # if none, then get the int equivalents of the hex characters
            r,g,b = int(col[0:2],16), int(col[2:4],16), int(col[4:6],16)
            colors = (r,g,b)
        else:
            sys.stderr.write(f'Invalid hex colors: {col}\n')
    elif col[0] == '(' and col[-1] == ')':
        r,g,b = col[1:-1].split(',')
        colors = (min(int(r),255),
                  min(int(g),255),
                  min(int(b),255))
    else:
        sys.stderr.write(f'Ignoring colors: {col}\n')
    print(f'{colors=}')

    return colors


def parse_colors_re(col: str):
    colors = 0
    match = re.search(r'^(\d{1,3})$|^([0-9a-f]{6})$|^\((\d{1,3}),(\d{1,3}),(\d{1,3})\)$',
                        col)
    if match:
        if match[1] != None:
            colors = max(0, min(255, int(col)))
        elif match[2] != None:
            colors = (int(col[0:2],16),
                      int(col[2:4],16),
                      int(col[4:6],16))
        else:
            colors = (min(int(match[3]),255),
                      min(int(match[4]),255),
                      min(int(match[5]),255))
    else:
        sys.stderr.write(f'Ignoring colors: {col}\n')
    print(f'{colors=}')

    return colors


class TestNewFunc(unittest.TestCase):
    def setUp(self):
        pass

    def test_func(self):
        pass


def main():
    args = command_line_args()

    with Image.open(args.filename) as image:
        inverted_image = invert(image)

    color = parse_colors(args.color)
    bg = Image.new('RGBA',
                   size=inverted_image.size,
                   color=color)
    bg.putalpha((100 - args.transparency) * 255 // 100)

    final = Image.alpha_composite(bg, inverted_image)
    if args.show:
        final.show()

    if args.outfile:
        outfile = args.outfile
    else:
        (fn, ext) = os.path.splitext(args.filename)
        outfile = fn+'-out'+ext
    final.save(outfile)


if __name__ == '__main__':
    # disable logging
    # logging.disable(logging.NOTSET)
    logging.disable(logging.CRITICAL)
    #unittest.main()

    main()
