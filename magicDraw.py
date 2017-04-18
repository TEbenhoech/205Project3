import cv2
import numpy as np
import math
#this is a comment

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
##Code based off code from opencv doc: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_mouse_handling/py_mouse_handling.html
ret, frame = video.read()
hand_cascade = cv2.CascadeClassifier('fist.xml')
height, width, channels = frame.shape
drawing = False # true if mouse is pressed
mode = False # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
brushSize = 10 #default size 10 brush
b = 0
g = 0
r = 200 #default to red brush

# mouse callback function
def draw_circle(event,x,y,flags,param):#commands you can use with keyboard testing only
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True#if left button on keyboard is pressed then draw with keyboard is true
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:#when drawing with keyboard you can choose different modes
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_LBUTTONUP:#this makes drawing false when left button is up
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)
            
            
img = np.zeros((height,width,3), np.uint8)
#ui = cv2.imread("UI.png")# reads and sets user interface to ui

while(1):#while this is true run!
   
    posX = 0 #initializes posX & posY containers to 0
    posY = 0
    ret, frame = video.read()#read video data sets it to frame and ret
    
    
    both = cv2.add(frame, img)#combines both frame  and img frame being hand detection and img being the actual video feed
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#sets our video box to have color
    hand = hand_cascade.detectMultiScale(gray,1.3,4)#this helps detect the hand 
    
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    

    for(x,y,w,h) in hand:
        #draws a rectangle around the fist 
        cv2.rectangle(frame,(x,y),(x+w, y+h),(b,g,r),2)
        posX = x+(w/2)
        posY = y+(h/2)
    
    eraser = (600,220, 0)#eraser detection 
    collisionX = posX - eraser[0]
    collisionY = posY - eraser[1]
    eraserCollision = math.sqrt((collisionX * collisionX) + (collisionY * collisionY))
    eraseFlag = True
    if eraserCollision < 35:#you can change this if you like to make the radius wider but 35 works well
        r = 0
        b = 0
        g = 0
        
    
    save = (310,50,0)#save detection
    colX = posX - save[0]
    colY = posY - save[1]
    saveCollision = math.sqrt((colX * colX)+ (colY * colY))
    saveFlag = True
    if saveCollision < 30:
        saveFlag = False
    
    small = (600,65,0)#small brush detection
    smallColX = posX - small[0]
    smallColY = posY - small[1]
    smallCollision = math.sqrt((smallColX * smallColX)+ (smallColY * smallColY))
    if smallCollision < 35:
        brushSize = 5
    
    norm = (600,100,0)#x, y coordiniates  normal brush detection
    normColX = posX - norm[0]
    normColY = posY - norm[1]
    normCollision = math.sqrt((normColX * normColX)+ (normColY * normColY))
    if normCollision < 35:
        brushSize = 10
    
    big = (600,150,0)#big brush detection 
    bigColX = posX - big[0]
    bigColY = posY - big[1]
    bigCollision = math.sqrt((bigColX * bigColX)+ (bigColY * bigColY))
    if bigCollision < 35:
        brushSize = 20
    
    red = (35,40,0) #red detection 
    redX = posX - red[0]#grabs x value
    redY = posY - red[1]#grabs y value 
    redCollision = math.sqrt((redX * redX)+ (redY * redY))#finds the radius
    if redCollision < 35:#if radius is less than 35 pixels then change brush to red this goes the same for all brushes, colors, save, and eraser
        g = 0
        r = 200
        b = 0



    
    orange = (35,90,0)#orange detection
    orangeX = posX - orange[0]
    orangeY = posY - orange[1]
    orangeCollision = math.sqrt((orangeX * orangeX)+ (orangeY * orangeY))
    if orangeCollision < 35:
        g = 100
        r = 255
        b = 0




    yellow = (35,150,0)
    yellowX = posX - yellow[0]
    yellowY = posY - yellow[1]
    yellowCollision = math.sqrt((yellowX * yellowX)+ (yellowY * yellowY))
    if yellowCollision < 35:
        g = 255
        r = 255
        b = 0
    
    green = (35,220,0)
    greenX = posX - green[0]
    greenY = posY - green[1]
    greenCollision = math.sqrt((greenX * greenX)+ (greenY * greenY))
    if greenCollision < 35:
        g = 200
        r = 0
        b = 0

    blue = (35,250,0)
    blueX = posX - blue[0]
    blueY = posY - blue[1]
    blueCollision = math.sqrt((blueX * blueX)+ (blueY * blueY))
    if blueCollision < 35:
        g = 0
        r = 0
        b = 200
    
    violet = (35,360,0)
    violetX = posX - violet[0]
    violetY = posY - violet[1]
    violetCollision = math.sqrt((violetX * violetX)+ (violetY * violetY))
    if violetCollision < 35:
        g = 0
        r = 200
        b = 255
   
    
    cv2.circle(img,(posX,posY),brushSize,(b,g,r),-1)#this calls our brush &draws it on screen using the cv2.circlefunction
    #cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF 
    if(eraseFlag == False):#this use to clear the whole screen but got replaces with a brush set to 0 , 0 , 0 
        img = np.zeros((height,width,3), np.uint8) 
    if(saveFlag == False): #checks if flag is false if so save frame when save icon is hovered over
        cv2.imwrite('YourImage.jpg',both)
    if k == ord('m'):
        mode = not mode
    if k == ord('s'): #manually saves using s key
        cv2.imwrite('test.jpg',both)
    if k == ord('c'):#clears whole screen using c key
        img = np.zeros((height,width,3), np.uint8)    
    elif k == 27 or k == ord('q'):#press esc or q to exit
        break
    
    #frame = cv2.add(frame,ui)#combines frame with ui 
    #both = cv2.addWeighted(frame,img)#combines everything together
    img2gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_inv = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR)
    cv2.imshow('test', mask)
    both = frame * (mask_inv / 255) + img * (mask / 255);
    both = cv2.flip(both, 1)#inverts the webcam screen
    cv2.imshow('image',both)#shows us our webcam with everything implemented, ui, hand detection and canvas

cv2.destroyAllWindows()#once while is false it exits the window
