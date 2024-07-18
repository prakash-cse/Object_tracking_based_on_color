import imutils #for resizing 
import cv2 #computer vision library



redLower =(100,17,49) #hsv values find from the callibration
redUpper =(167,174,193) #lower hsv values

camera=cv2.VideoCapture(0) #initializing the video capture

while True: #infinite loop for reading the camera frame
    (grabbed, frame) = camera.read() #read the frame from the camera
    frame = imutils.resize(frame, width=600) #resized of the image obtained from the camera
    blurred = cv2.GaussianBlur(frame, (11,11), 0) #smoothening of the image
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) #image from bgr to the hsv values
    mask = cv2.inRange(hsv, redLower, redUpper) #masking of the specific identifying object color only one color
    mask = cv2.erode(mask, None, iterations=2) #errosion & dilation remove of the holes and noise and other things
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] #this counters will connect the points on the edges of the image to identify the image(and also if the according to the count the possibility of the image will be)
    center = None #to find the center for upcoming scenario

    if len(cnts) > 0: #if the count occurs only the it will draw the ciricle and identify the centroid
        c = max(cnts, key=cv2.contourArea) #to identify the maximum contour area
        ((x,y), radius) = cv2.minEnclosingCircle(c) #drawing of the minimum enclosure circle with the valu of c
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"])) #this statement center is for getting the center value of the image
        if radius > 10: #according to some radius only the ciricle will be drawn
             cv2.circle(frame, (int(x),int(y)),int (radius),(0,255,255),2) #syntax for drwing the circle
             cv2.circle(frame, center,5,(0,0,255), -1) # this to plot a thick dot point at the center of the circle

             if radius > 250: #if the object is too far away for plotting the radius this condition works
                 print("stop")
             else:
                 if(center[0]<150):
                    print("Left")
                 elif(center[0]>450):
                    print("Right")
                 elif(radius<250):
                    print("Front")
                 else:
                     print("Stop")
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
