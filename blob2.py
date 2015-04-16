__author__ = 'mandeep'
import cv2
import numpy as np

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

#greeen
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


def find_hsv(hsv):
    global minhws,maxhws,hwmins,hwmaxs

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

_,frame = cap.read()

# smooth it
frame = cv2.blur(frame,(3,3))

get_r(frame)
# convert to hsv and find range of colors
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
find_hsv(hsv)

print minhws
print maxhws
print hwmins
print hwmaxs

color_min=[minhws[0],hwmins[1],80]
color_max=[maxhws[0],hwmaxs[1],255]
while(1):

    # read the frames
    _,frame = cap.read()

    # smooth it
    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv,np.array((color_min[0], color_min[1], 80)), np.array((color_max[0], color_max[1], 255)))
    thresh2 = thresh.copy()

    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

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
    if cv2.waitKey(33)== 27:
        break



# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()