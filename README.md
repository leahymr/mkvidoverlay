# mkvidoverlay
## Make Video Overlay

## Purpose
A client needed a routine that would take a .png graphic, invert it,
and add a black background (60% transparent).
The resulting graphic (.png) would be used as an overlay for streaming video
broadcasts.

## Requirement
Must install the Pillow module. \
`pip install PIL`

## Syntax
```
mkvidoverlay.py
   [-h|--help]              # help message
   [-s|--show]              # show the created picture(s)
   [-o|--outpath OUTPATH]   # specify the folder where output files will be saved
                            # (e.g., -o '~/Pictures')
   [-a|--append APPEND]     # append this string to the basename of the output file
                            # (e.g., -a 'new':  'pic.png' -> 'pic-new.png')
                            # DEFAULT: 'out'
   [-c|--color COLOR]       # Three ways to denote color:
                            # 1. integer: 0-255 (0=black, 255=white)
                            # 2. three hex numbers: rrggbb e.g. '2244ee'
                            # 3. three numbers: '(rr,gg,bb)' e.g. '(22,44,163)'
                            # DEFAULT: 0
   [-t|--transparency {0,10,20..90,100}] # Transparency of the background
                            #  (0=opaque,100=transparent)
                            # DEFAULT: 40
   filename [filename...]   # one or more filenames
```