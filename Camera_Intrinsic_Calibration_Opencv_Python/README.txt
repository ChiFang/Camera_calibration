Environment:

OS: WIN10
Python version: 2.7 64bits
OpenCV Version: 2.4.9


Output:

1. Intrinsic matrix
2. Distortion coefficients

Note:

Capture_K_Image.py:

use for capture image for calibration
press 's' or 'S' to capture and Esc to quit
captured image will be in folder named "K_Img" in current direction


calibrate_2_4_x.py:

use for camera calibration

USAGE = '''
USAGE: calib.py [--save <filename>] [--debug <output path>] [--square_size] [<image mask>]
'''

ex:
python calibrate_2_4_x.py --save K_Result.txt --debug K_Result --square_size 26 ./K_Img/K_Img_*.png

if you want to use opencv 3.x, you need to modify a little bit "calibrateCamera" related function like parameter
