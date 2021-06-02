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


def command_line_args() -> argparse:
    parser = argparse.ArgumentParser(
                description="Invert an image and add a black background "
                            "that has TRANSPARENCY% of transparency")
    parser.add_argument("filename",
                        nargs='+',
                        help="image file(s)")
    parser.add_argument("-t", "--transparency",
                        type=int,
                        choices=range(0,101,10),
                        default=40,
                        help="transparency of background (integer %)")
    parser.add_argument("-s", "--show",
                        help="display image",
                        action='store_true')
    parser.add_argument("-o", "--outpath",
                        help="output path name")
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

    return colors


class TestNewFunc(unittest.TestCase):
    def setUp(self):
        pass

    def test_func(self):
        pass


def main():
    args = command_line_args()

    for file in args.filename:
        try:
            file = os.path.abspath(file)
            # Errors will be caught by the try, and the rest of the routine will be skipped
            with Image.open(file) as image:
                inverted_image = invert(image)

            color = parse_colors(args.color)
            bg = Image.new('RGBA',
                           size=inverted_image.size,
                           color=color)
            bg.putalpha((100 - args.transparency) * 255 // 100)

            final = Image.alpha_composite(bg, inverted_image)
            if args.show:
                final.show()

            # Break apart the file name and prepare to save the file in a different
            # folder if necessary
            (path, fn) = os.path.split(file)
            (fn, ext) = os.path.splitext(fn)
            outfile = fn+'-out'+ext
            if args.outpath:
                outfile = os.path.join(args.outpath, outfile)

            # Special try for writing the file
            try:
                final.save(outfile)
            except PermissionError as err:
                print(f"Can't write file: {err}")
            except:
                raise

        except PermissionError as err:
            print(f"Can't read file: {err}")
        except:
            print("Unexpected error:", sys.exc_info()[1])
            sys.exit(2)


if __name__ == '__main__':
    # disable logging
    # logging.disable(logging.NOTSET)
    logging.disable(logging.CRITICAL)
    #unittest.main()

    main()
