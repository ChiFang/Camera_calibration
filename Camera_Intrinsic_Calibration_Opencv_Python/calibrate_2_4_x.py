#!/usr/bin/env python

import numpy as np
import cv2
import os
from common import splitfn

USAGE = '''
USAGE: calib.py [--save <filename>] [--debug <output path>] [--square_size] [<image mask>]
'''



if __name__ == '__main__':
    import sys, getopt
    from glob import glob

    args, img_mask = getopt.getopt(sys.argv[1:], '', ['save=', 'debug=', 'square_size='])
    args = dict(args)
    
    
    try: img_mask = img_mask[0]
    except: img_mask = './K_Img/K_Img_*.png'
    img_names = glob(img_mask)
    debug_dir = args.get('--debug')
    square_size = float(args.get('--square_size', 1.0))
    
    try: LogFileName = args.get('--save')
    except: LogFileName = 'log.txt'
    
    if debug_dir:
        LogFileName = debug_dir + '/' + LogFileName
        

    pattern_size = (9, 6)
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = 0, 0
    
    for fn in img_names:
        print 'processing %s...' % fn,
        img = cv2.imread(fn, 0)
        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        
        if found:
            term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
        if debug_dir:
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, pattern_size, corners, found)
            path, name, ext = splitfn(fn)   #name = fn
            cv2.imwrite('%s/%s_chess.bmp' % (debug_dir, name), vis)
        if not found:
            print 'chessboard not found'
            continue
        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print 'ok'

    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h))
    print "\n\n-------------\nCalibration Resul:\n"
    print "RMS:", rms
    print "camera matrix:\n", camera_matrix
    print "distortion coefficients: ", dist_coefs.ravel()
    print "-------------\n\n"
    cv2.destroyAllWindows()
    
    
    print "save log file..."
    fo=open(LogFileName, 'w')
    fo.write("Calibration log:\n")
    fo.write("RMS: %f\n\n" % (rms))
    fo.write("Intrinsic Matrix:\n")
    fo.write("%f\t%f\t%f\n" % (camera_matrix[0][0], camera_matrix[0][1], camera_matrix[0][2]))
    fo.write("%f\t%f\t%f\n" % (camera_matrix[1][0], camera_matrix[1][1], camera_matrix[1][2]))
    fo.write("%f\t%f\t%f\n\n" % (camera_matrix[2][0], camera_matrix[2][1], camera_matrix[2][2]))  
    fo.write("distortion coefficients:\n")
    dist_coefs = dist_coefs.ravel()
    for coef in dist_coefs:
        fo.write("%f\t" % (coef))
    fo.close()
    print "Done"
