# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 11:15:01 2017

@author: aokeke
"""
import qrcode
from PIL import Image
import cv2
import zbar
import numpy as np
#import copy

def makeCodes():
    shoeimg = qrcode.make('shoe')
    shoeimg.save("shoe.png",format="png")
    
    phoneimg = qrcode.make('phone')
    phoneimg.save("phone.png",format="png")
    
def detect_qr(image):
    # create a reader
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    # obtain image data
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY,dstCn=0)
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()


    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    symbols = []
    for symbol in image:
        symbols.append(symbol)
        # do something useful with results
#        if symbol.data == "None":
#            return "no data in this symbol"
#        else:
#            return symbol
    return symbols
            
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:    
    try:
        ret, frame = cap.read()
        if ret:
            symbols = detect_qr(frame)
            if len(symbols)>0:
                lastSyms = symbols
                contours = []
                specialCnt = []
                for s in symbols:
                    print ("data:",s.data)
                    contours.append(np.array(s.location))
                    if s.data=="shoe":
                        specialCnt.append(np.array(s.location))
                cv2.drawContours(frame,contours,0,(0,0,255),2)
                if len(specialCnt)>0:
                    cv2.drawContours(frame,specialCnt,0,(255,0,255),2)
                
                for s in symbols:
                    try:                    
                        w,x1,y1,z = s.location
                        a,b = w
                        c,d = x1
                        e,f = y1
                        g,h = z

                        x = int(float(a+c+e+g)/4)
                        y = int(float(b+d+f+h)/4)
                        cv2.putText(frame,s.data,(x,y), font, 0.5, (11,255,255), 2, cv2.LINE_AA)
                    except:
                        pass


            cv2.imshow("Original", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
#            break
        else:
            print "couldn't take image"


    except KeyboardInterrupt:
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
