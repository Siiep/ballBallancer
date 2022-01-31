#testing file for Color tracking input_code file.

import cv2
import numpy as np
from PIL import Image
def PIX(event, x, y, flags, param):         # This function is used to open the pixel window and display values
    if event == cv2.EVENT_LBUTTONDBLCLK:
        r,g,b = rgbimg.getpixel((x,y))
        txt = str(r)+","+str(g)+","+str(b)
        bg = np.zeros((200,400,3), np.uint8)
        bg[:,0:400] = (b,g,r)
        font = cv2.FONT_ITALIC
        cv2.putText(bg,txt,(10,100),font,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('rgb',bg)


cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    flipped = cv2.flip(frame, 1)
    cv2.imshow('vid',flipped)
    if cv2.waitKey(1) & 0xFF == ord('c'): # Press C to enter the code block 
        cv2.imwrite('1.png',flipped)    # Creates a snapshot of the video
        imge = Image.open('1.png')      # Opens the snapshot in a seperate window
        rgbimg = imge.convert('RGB')    # Converts Pixel Data to the RGB standard
        cv2.imshow('pic',flipped)       # function that captures the current pixel -
                                        # - displays it on the video feed window
        cv2.setMouseCallback('pic',PIX) # Updates the pixel chosen on the windows
    elif cv2.waitKey(1) & 0xFF == ord(' '): # hit space to quit
        break
cap.release()
cv2.destroyAllWindows()
