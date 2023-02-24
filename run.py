#!/usr/bin/env python3

import subprocess
import argparse
import PIL.Image
import math

# parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("mu", type=float)
args = ap.parse_args()

# Crop image if necessary
img = PIL.Image('input_0.png')
(sizeX, sizeY) = img.size
cropsize = (min(sizeX, 450), min(sizeY, 450))

if (sizeX, sizeY) != cropsize:
    (x0, y0) = (int(math.floor((sizeX - cropsize[0])/2)),
        int(math.floor((sizeY - cropsize[1])/2)))
    img.crop((x0, y0, x0 + cropsize[0], y0 + cropsize[1]))
    img.save('input_0_sel.png')


# Run chanvese
subprocess.run(['chanvese', 
        'mu:' + str(args.mu),
        'tol:-1', 'maxiter:100', 'iterperframe:5',
        'input_0_sel.png', 'evolution.gif', 'segmentation.png'])

zoomfactor = int(max(2,math.floor(600.0/max(cropsize[0],cropsize[1]))))
(sizeX, sizeY) = (zoomfactor*cropsize[0], zoomfactor*cropsize[1])

for filename in ['input_0_sel', 'segmentation']:
    im = PIL.Image(filename + '.png')
    im.resize((sizeX, sizeY), method='nearest')
    im.save(filename + '_zoom.png')
