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


def main():
    args = command_line_args()

    with Image.open(args.filename) as image:
        inverted_image = invert(image)

    bg = Image.new('RGBA',
                   size=inverted_image.size,
                   color=0)
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
