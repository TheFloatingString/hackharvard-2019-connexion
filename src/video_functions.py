import cv2
import os
from src.gcloud_functions import get_prediction,filepath_to_char


def main(filepath):
    vidcap = cv2.VideoCapture(filepath)
    return get_text(filepath, vidcap)

def getFrame(sec, vidcap):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    t=0
    if hasFrames:
        cv2.imwrite("static/image.jpg", image)     # save frame as JPG file
        t=1
    return t


def get_text(path, vidcap):
    text=""
    sec = 0
    frameRate = 1 #//it will capture image in each 0.5 second
    count=0
    success = getFrame(sec, vidcap)
    letter={}
    while success:
        count = count + 1
        print(count)
        sec = sec + frameRate
        sec = round(sec, 2)
        t=filepath_to_char("static/image.jpg")
        #print("t = ",t)
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
        success=getFrame(sec, vidcap)
        #print("Text = ",text)
    return text

if __name__ == '__main__':
    path="static/video.mp4"
    vidcap=cv2.VideoCapture(path)
    print(get_text(path))