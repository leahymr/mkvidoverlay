#!/usr/bin/env python3

import argparse, sys, os

try:
    from PIL import Image, ImageOps
except:
    print('This program requires the Pillow library:')
    print('  pip install Pillow')
    sys.exit(1)

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
                        help="background color (0-255 or rrggbb)",
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
    else:
        sys.stderr.write(f'Ignoring colors: {col}\n')
    print(f'{colors=}')

    return colors

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


main()
