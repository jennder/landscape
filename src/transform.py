import os
import cv2
import numpy as np

def get_transform(dir, func):
    for filename in os.listdir(dir):
        if 'DS_Store' in filename:
            continue
        get_one(dir, filename, func)

def get_one(path, filename, func):
    path = os.path.join(path, filename)
    img = cv2.imread(path)
    out = func(img)
    cv2.imwrite(filename, out)

def hough_lines(img):
    mono = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(mono, 200, 400)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=50)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img, (x1, y1), (x2, y2), (200, 200, 200), 1)
    return img

def canny_edge(img):
    mono = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(mono, 75, 150)
    return edges

def hough_circle(img):
    bg = cv2.imread('../assets/bg.jpg')
    resized = cv2.resize(img,(600, 400),interpolation = cv2.INTER_AREA)
    mono = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(mono,cv2.HOUGH_GRADIENT,1,20,
                                param1=30,param2=15,minRadius=0,maxRadius=0)

    circles = np.uint16(np.around(circles))

    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(bg,(i[0]*10,i[1]*10),i[2]*10,(200,200,200),1)

    return bg

get_transform('../assets/', hough_circle)
#get_one('../assets/20200920-fens-0003.JPG', hough_circle)