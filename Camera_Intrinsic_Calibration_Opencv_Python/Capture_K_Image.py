import numpy as np
import cv2
import os

dir_name = "./K_Img"
if not os.path.exists(dir_name):
    print ("miss folder, regenerate it")
    os.makedirs(dir_name)
else:
    print ("folder exists")


CapCnt = cv2.VideoCapture()
CamCnt = 0
while(True):
    if CapCnt.open(CamCnt) == 0:
        break
    else:
        CamCnt = CamCnt+1
       
print (str(CamCnt) + " camera detected")
CapCnt.release()

while(True):
    try:
        ID = int(input('camer index: ')) # make sure ID is int type in both python 2.x and 3.x
        if (ID < CamCnt) and (ID >= 0):
            print ("acceptable ID")
            break
        else:
            print ("unacceptable ID")
    except:
        print("please input a interger...")

    

print('start to use camera', ID)

cap = cv2.VideoCapture(ID)
cnt = 0
    
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    
    PressKey = cv2.waitKey(10)
    PressKey = PressKey & 0xFF
    if PressKey == 27:  ## Esc
        print ("Quit")
        break
    elif (PressKey == ord('s')) or (PressKey == ord('S')):
        name = "./K_Img/K_Img_" + str(cnt) + ".png"
        print (name)
        cv2.imwrite(name, frame)
        cnt = cnt + 1
        

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()