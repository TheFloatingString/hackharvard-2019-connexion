import cv2
import os
from gcloud_functions import get_prediction,filepath_to_char


def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    t=0
    if hasFrames:
        cv2.imwrite("static/image.jpg", image)     # save frame as JPG file
        t=1
    return t


def get_text(path):
    text=""
    sec = 0
    frameRate = 0.75 #//it will capture image in each 0.5 second
    count=0
    success = getFrame(sec)
    letter={}
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        t=filepath_to_char("static/image.jpg").lower()
        print("t = ",t)
        if t=='nothing':
            mct=0
            mchar=''
            for i in letter:
                if letter[i]>mct:
                    mct=letter[i]
                    mchar=i
            print("char rn :" ,mchar)
            mchar=mchar.lower()
            letter={}
            if (mchar>='a' and mchar<='z' and len(mchar)==1):
                text+=mchar
            elif mchar=="space":
                text+=" "
            elif mchar=="del":
                text=text[0:len(text)-1]
            #print("Char rn :",mchar)
            #print("Text = ",text)
            mct=0
            mchar=0
        else:
            if t in letter:
                letter[t]+=1
            else:
                letter[t]=1
        os.remove("static/image.jpg")
        success=getFrame(sec)
        #print("Text = ",text)
    return text

path="static/video.mp4"
vidcap=cv2.VideoCapture(path)
print(get_text(path))