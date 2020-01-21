  #initiate vedio
#frame
#convert into hsv
#define count
#count <3
###{ red_frame
##   blue_frame
##   contures of red {
##       r_x_cordinate
##       rotate in direction of r_x_cordinate till centre is alligned(
##           rotate some degree()
##           return to take_frame()
##        )
##       if blue is allined with red{
##           start rotating till another red contur is found
##           recurssive for new r_x_cordiate
##           }
##       move forward(
##           in (red image >75%){
##               stop()
##               red led on()
##               cout++
##               take_frame()
##               )
##       


import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
arduino = serial.Serial('COM4',9600) #Create Serial port object called arduinoSerialData
time.sleep(2) #wait for 2 secounds for the communication to get established

cap = cv2.VideoCapture(0)
##cap = cv2.VideoCapture('test_ved.mp4')

count =0

##ret, image = cap.read()
##image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
##centre_x  , image_total_area= (image.shape[0])/2 , (image.size)/3
##print(centre_x  , image_total_area)

def analyze_frame(lower_red,upper_red):
    ret, image = cap.read()
##    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
##    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)

    image_HSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_HSV,lower_red,upper_red)
    mask = cv2.GaussianBlur(mask,(5,5),0)
    contours, hierarchy =cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # If we have at least one contour, look through each one and pick the biggest
    print(len(contours))
    largest = 0
    area = 0
    if (len(contours)==0):
        return 0,0,0
    else:    
        for i in range(len(contours)):
            # get the area of the ith contour
            temp_area = cv2.contourArea(contours[i])
            # if it is the biggest we have seen, keep it
            if temp_area > area:
                area = temp_area
                largest = i
        coordinates = cv2.moments(contours[largest])
        target_x = int(coordinates['m10']/coordinates['m00'])
        target_y = int(coordinates['m01']/coordinates['m00'])
        return target_x, target_y,area
while(True):
    ret, image = cap.read()
##    cv2.imshow("image",image)
##    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
    centre_x  , image_total_area= (image.shape[0])/2 , (image.size)/3
    print(centre_x  , image_total_area)


    if(count<3):
        r_x_cor,r_y_cor,r_area =analyze_frame(np.array([79,111,81]),np.array([153,255,255]))
        b_x_cor,b_y_cor,b_area =analyze_frame(np.array([86,204,127]),np.array([255,255,255]))
##        print(r_x_cor,r_y_cor,r_area,b_x_cor,b_y_cor,b_area)
        if(r_x_cor< 0.8*centre_x):
            print('L')
            if(r_area>0.65*image_total_area):
                count+=arduino.readline()
                print("red block has been pick"+str(count)+"times")
                pass
            arduino.write(b'L')
            arduino.write(b'S')
            print('S')
            pass
        elif(r_x_cor<1.2*centre_x):
            if(r_area>b_area): 
                print('F')
                if(r_area>0.65*image_total_area):
                    count+=arduino.readline()
                    print("red block has been pick"+str(count)+"times")
                    pass
                arduino.write(b'F')
                time.sleep(2)
                pass
            else:
                if(b_x_cor>1.25*centre_x or b_x_cor<0.75*centre_x):
                    print(str(3)+'F and blue is far away')
                    if(r_area>0.65*image_total_area):
                        count+=arduino.readline()
                        print("red block has been pick"+str(count)+"times")
                        pass
                    arduino.write(b'F')
                    time.sleep(2)
                    pass
                elif(b_x_cor>=r_x_cor):
                    print(str(4)+'L to counter blue')
                    if(r_area>0.65*image_total_area):
                        count+=arduino.readline()
                        print("red block has been pick"+str(count)+"times")
                        pass
                    arduino.write(b'L')
                    pass
                elif(b_x_cor<=r_x_cor):
                    print(str(5)+'R to counter blue')
                    if(r_area>0.65*image_total_area):
                        count+=arduino.readline()
                        print("red block has been pick"+str(count)+"times")
                        pass
                    arduino.write(b'R')
                    pass    
    
        else:
            print(str(6)+'R to alline red')
            
            arduino.write(b'R')
##            arduino.write(b'S')
            if(r_area>0.65*image_total_area):
                count+=arduino.readline()
                print("red block has been pick"+str(count)+"times")
                pass
            pass

            
    else if(count==3):
        print('else')
        ret, frame = cap.read()
        b_x_cor,b_y_cor,b_area =analyze_frame(np.array([100,134,88]),np.array([107,255,255]))
        g_x_cor,g_y_cor,g_area =analyze_frame(np.array([15,50,95]),np.array([90,255,245]))
        if(g_x_cor<0.8*centre_x):
            if(g_area>0.65*image_total_area):
                count+=arduino.readline()
                print("red block has been pick"+str(count)+"times")
                pass
            arduino.write(b'L')
            arduino.write(b'S')
            pass
        elif(g_x_cor<1.2*centre_x):
            if(g_area>b_area):
                if(g_area>0.65*image_total_area):
                    count+=arduino.readline()
                    print("red block has been pick"+str(count)+"times")
                    pass
                arduino.write(b'F')
                time.sleep(2)
                pass
            else:
                if(b_x_cor>1.25*centre_x or b_x_cor<0.75*centre_x):
                    if(g_area>0.65*image_total_area):
                        count+=arduino.readline()
                        print("red block has been pick"+str(count)+"times")
                        pass
                    arduino.write(b'F')
                    time.sleep(2)
                    pass
                elif(b_x_cor>=g_x_cor):
                    if(r_area>0.65*image_total_area):
                        count+=arduino.readline()
                        print("red block has been pick"+str(count)+"times")
                        pass
                    arduino.write(b'L')
    
                    pass
                elif(b_x_cor<=g_x_cor):
                    if(r_area>0.65*image_total_area):
                        count+=arduino.readline()
                        print("red block has been pick"+str(count)+"times")
                        pass
                    arduino.write(b'R')
                    pass    
        else:
            if(g_area>0.65*image_total_area):
                count+=arduino.readline()
                print("red block has been pick"+str(count)+"times")
                pass
            arduino.write(b'R')   
            arduino.write(b'S')
            pass

    else:
        arduino.write(b'S')
        print("the task has completed")
        break 
        


cap.release()
cv2.destroyAllWindows()            







        

           


