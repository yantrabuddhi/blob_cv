__author__ = 'mandeep'
import cv2
import numpy as np
import time
# create video capture
cap = cv2.VideoCapture(0)
x1=0
y1=0
x2=0
y2=0
stat=0

minhws=[]
maxhws=[]
hwmins=[]
hwmaxs=[]

bgr_max=[0,0,0]
bgr_min=[255,255,255]


minhws2=[]
maxhws2=[]
hwmins2=[]
hwmaxs2=[]

bgr_max2=[0,0,0]
bgr_min2=[255,255,255]


blur_size=4
#green blur 4 (max for monitor cam)
#[ 39 161 173]
#[ 54 123 135]
#[ 42  99 201]
#[ 41 249 120]

#greeen -blur 3
#[ 38 158 155]
#[ 63 126 105]
#[ 59 115 104]
#[ 43 255  93]


#Blue
#[107 214 255]
#[118 163 240]
#[117 144 249]
#[111 250 255]

def OnMouse(event,x,y,fl,no):
    global x1,x2,y1,y2,stat
    if stat>1:return
    if event!=cv2.EVENT_LBUTTONDOWN:
        x2=x
        y2=y
        return
    if stat==0:
        x1=x
        y1=y
        stat=1
    else:
        x2=x
        y2=y
        stat=2


def get_r(frm):
    global x1,x2,y1,y2,stat
    stat=0
    cv2.namedWindow("cap")
    cv2.imshow("cap",frm)
    cv2.setMouseCallback("cap",OnMouse)
    while(stat<2):
        if (stat==1):
            im2=frm.copy()
            cv2.rectangle(im2,(x1,y1),(x2,y2),(0,0,255,0),2,8,0)
            cv2.imshow("cap",im2)
        cv2.waitKey(10)
    cv2.destroyWindow("cap")

def get_r2(frm):
    global x1,x2,y1,y2,stat
    stat=0
    cv2.namedWindow("cap2")
    cv2.imshow("cap2",frm)
    cv2.setMouseCallback("cap2",OnMouse)
    while(stat<2):
        if (stat==1):
            im2=frm.copy()
            cv2.rectangle(im2,(x1,y1),(x2,y2),(0,0,255,0),2,8,0)
            cv2.imshow("cap2",im2)
        cv2.waitKey(10)
    cv2.destroyWindow("cap2")

def find_rgb_r(frm):
    global bgr_max,bgr_min,x1,y1,x2,y2
    for x in range(x1,x2,1):
        for y in range(y1,y2,1):
            bgr=frm[y,x]
            for cn in range(0,3):
                if bgr[cn]>bgr_max[cn]:bgr_max[cn]=bgr[cn].copy()
                if bgr[cn]<bgr_min[cn]:bgr_min[cn]=bgr[cn].copy()

def find_rgb_r2(frm):
    global bgr_max2,bgr_min2,x1,y1,x2,y2
    for x in range(x1,x2,1):
        for y in range(y1,y2,1):
            bgr=frm[y,x]
            for cn in range(0,3):
                if bgr[cn]>bgr_max2[cn]:bgr_max2[cn]=bgr[cn].copy()
                if bgr[cn]<bgr_min2[cn]:bgr_min2[cn]=bgr[cn].copy()


def find_hsv(hsv):
    global minhws,maxhws,hwmins,hwmaxs,x1,y1,x2,y2

    #we have the x1,y1,x2,y2
    #print hsv[y1,x1]
    hsr=hsv[y1,x1]
    minhws=hsr.copy()
    maxhws=hsr.copy()
    hwmins=hsr.copy()
    hwmaxs=hsr.copy()

    for x in range(x1,x2,1):
        for y in range(y1,y2,1):
            pix=hsv[y,x]
            hp=pix[0]
            sp=pix[1]
            vp=pix[2]
            if hp<minhws[0]:
                minhws[0]=hp
                minhws[1]=sp
                minhws[2]=vp
            if hp>maxhws[0]:
                maxhws[0]=hp
                maxhws[1]=sp
                maxhws[2]=vp
            if sp<hwmins[1]:
                hwmins[0]=hp
                hwmins[1]=sp
                hwmins[2]=vp
            if sp>hwmaxs[1]:
                hwmaxs[0]=hp
                hwmaxs[1]=sp
                hwmaxs[2]=vp
            #look for h and s h1,s1 h2,s1 h1,s2 h2,s2

def find_hsv2(hsv):
    global minhws2,maxhws2,hwmins2,hwmaxs2,x1,y1,x2,y2

    #we have the x1,y1,x2,y2
    #print hsv[y1,x1]
    hsr=hsv[y1,x1]
    minhws2=hsr.copy()
    maxhws2=hsr.copy()
    hwmins2=hsr.copy()
    hwmaxs2=hsr.copy()

    for x in range(x1,x2,1):
        for y in range(y1,y2,1):
            pix=hsv[y,x]
            hp=pix[0]
            sp=pix[1]
            vp=pix[2]
            if hp<minhws2[0]:
                minhws2[0]=hp
                minhws2[1]=sp
                minhws2[2]=vp
            if hp>maxhws2[0]:
                maxhws2[0]=hp
                maxhws2[1]=sp
                maxhws2[2]=vp
            if sp<hwmins2[1]:
                hwmins2[0]=hp
                hwmins2[1]=sp
                hwmins2[2]=vp
            if sp>hwmaxs2[1]:
                hwmaxs2[0]=hp
                hwmaxs2[1]=sp
                hwmaxs2[2]=vp
            #look for h and s h1,s1 h2,s1 h1,s2 h2,s2


cv2.namedWindow("brt")
while(1):
    _,frame = cap.read()
    cv2.imshow("brt",frame)
    if cv2.waitKey(33)==1048603:break

cv2.destroyWindow("brt")

# smooth it
frame = cv2.blur(frame,(blur_size,blur_size))#3,3

get_r(frame)
find_rgb_r(frame)

# convert to hsv and find range of colors
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
find_hsv(hsv)


cv2.namedWindow("brt2")
while(1):
    _,frame = cap.read()
    cv2.imshow("brt2",frame)
    if cv2.waitKey(33)==1048603:break

cv2.destroyWindow("brt2")

# smooth it
frame = cv2.blur(frame,(blur_size,blur_size))#3,3

get_r2(frame)
find_rgb_r2(frame)

# convert to hsv and find range of colors
hsv2 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
find_hsv2(hsv2)


print minhws
print maxhws
print hwmins
print hwmaxs
print "bgr"
print bgr_min
print bgr_max
for ix in range(0,3):
    if bgr_max[ix]<bgr_max2[ix]:bgr_max[ix]=bgr_max2[ix].copy()
    if bgr_min[ix]>bgr_min2[ix]:bgr_min[ix]=bgr_min2[ix].copy()

minv=minhws[2].copy()
if minv>maxhws[2]:minv=maxhws[2].copy()
if minv>hwmins[2]:minv=hwmins[2].copy()
if minv>hwmaxs[2]:minv=hwmaxs[2].copy()

if minv>maxhws2[2]:minv=maxhws2[2].copy()
if minv>hwmins2[2]:minv=hwmins2[2].copy()
if minv>hwmaxs2[2]:minv=hwmaxs2[2].copy()

maxv=minhws[2].copy()
if maxv<maxhws[2]:maxv=maxhws[2].copy()
if maxv<hwmins[2]:maxv=hwmins[2].copy()
if maxv<hwmaxs[2]:maxv=hwmaxs[2].copy()

if maxv<maxhws2[2]:maxv=maxhws2[2].copy()
if maxv<hwmins2[2]:maxv=hwmins2[2].copy()
if maxv<hwmaxs2[2]:maxv=hwmaxs2[2].copy()

if (0):#gives error in bright colors thresholding?dont know why?numpy data type error
    if minv>90:minv=minv-10
    if maxv<240:maxv=maxv+10
    print minv
    print maxv

if(0):
    minv=90
    maxv=250

color_min=[minhws[0],hwmins[1],minv]#80
color_max=[maxhws[0],hwmaxs[1],maxv]#255

if (0):
    vl=0.85#0.8,0.9
    for ii in range(0,3):
        bgr_min[ii]=int(bgr_min[ii]*vl)
        #bgr_max[ii]=int(bgr_max[ii]*1.2)

#cv2.namedWindow("rthresh")
while(1):

    # read the frames
    _,frame = cap.read()

    # smooth it
    frame = cv2.blur(frame,(blur_size,blur_size))
    rthresh=cv2.inRange(frame,np.array((bgr_min[0],bgr_min[1],bgr_min[2]),dtype = "uint8"),np.array((bgr_max[0],bgr_max[1],bgr_max[2]),dtype = "uint8"))
    rt=rthresh.copy()
    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv,np.array((color_min[0], color_min[1], color_min[2]),dtype = "uint8"), np.array((color_max[0], color_max[1], color_max[2]),dtype = "uint8"))
    #thresh=cv2.blur(thresh1,(blur_size,blur_size))
    #thresh = cv2.inRange(hsv,np.array((color_min[0], 40, color_min[2])), np.array((color_max[0], 250, color_max[2])))
    thresh2 = thresh.copy()

    output1=cv2.bitwise_and(rt,thresh)
    #output=cv2.blur(output1,(blur_size,blur_size))
    output=cv2.erode(output1,(blur_size,blur_size))
    see=output.copy()
    # find contours in the threshold image
    #contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    contours,hierarchy = cv2.findContours(output,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(frame,(cx,cy),5,255,-1)

    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('frame',frame)
    cv2.imshow('thresh',thresh2)
    cv2.imshow('rt',rt)
    cv2.imshow('output',see)
    if cv2.waitKey(33)== 1048603:#27
        break



# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()