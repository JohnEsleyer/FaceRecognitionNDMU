
import tkinter
import PIL.Image, PIL.ImageTk
import cv2 
import face_recognition 
import time 
import os 
from datetime import datetime
import numpy as np 

path = 'images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
 
encodeListKnown = findEncodings(images)
print('Encoding Complete')


#==================================
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window 
        self.window.geometry("720x360") 
        self.window.title(window_title)
        self.video_source = video_source 
        self.vid = MyVideoCapture(video_source)

        self.frame = tkinter.Frame(
            self.window, 
            height=360)
        self.frame.pack() 

        self.centerFrame = tkinter.Frame(self.window)
        self.centerFrame.pack() 


        self.photo_image = PIL.ImageTk.PhotoImage(file="ndmu.png")
        self.cv1 = tkinter.Canvas(
            self.frame, 
            width=self.photo_image.width(),
            height=self.photo_image.height()
        )

        self.cv1.pack(side="bottom")

        self.cv1.create_image(
            0,
            0,
            image=self.photo_image,
            anchor=tkinter.NW
        )

        self.regButton = tkinter.Button(
            self.centerFrame,
            text="Register Face",
            width=30
        )
        self.regButton.pack()

        self.detButton = tkinter.Button(
            self.centerFrame,
            text="Detect Face",
            width=30,
            command=self.detectFace
        )
        self.detButton.pack()



        self.window.mainloop()

    def detectFace(self):
        print("detectFace")
        for widgets in self.window.winfo_children():
            widgets.destroy()
        self.frame = tkinter.Frame(self.window).pack(side="top")
        self.cv2 = tkinter.Canvas(
            self.frame,
            width=self.vid.width,
            height=self.vid.height
        )
        self.cv2.pack()
        self.delay = 15
        self.update()

 
    def snapshot(self):
        #Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.cv2.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_frame(self):
        success, img = self.vid.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
    
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
        #=============================
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
