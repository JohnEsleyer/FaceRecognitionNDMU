
import tkinter
import PIL.Image, PIL.ImageTk
import cv2 
import face_recognition 
import time 
import os 
from datetime import datetime
import numpy as np 


# displayName = "Hello World"

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
        self.save_name = "None"
        self.firstTime = True
        self.menuScreen()
        self.firstTime = False
        self.window.mainloop()

    
    def menuScreen(self):
        if not self.firstTime:
            for widgets in self.window.winfo_children():
                widgets.destroy()

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
            width=30,
            command=self.registerFace
        )
        self.regButton.pack()

        self.detButton = tkinter.Button(
            self.centerFrame,
            text="Detect Face",
            width=30,
            command=self.detectFace
        )
        self.detButton.pack()
    def registerFace(self):
        for widgets in self.window.winfo_children():
            widgets.destroy()
        
        self.frame = tkinter.Frame(self.window).pack(side="top")
        self.tmpCav1 = tkinter.Canvas(
            self.frame, 
            height=300,
            width=1
        ).pack()

       

        self.text1 = tkinter.StringVar()
        self.labelName = tkinter.Label(
            self.frame,
            textvariable=self.text1,
            font=("Helvetica", 19)
        )

        self.labelName.pack()
        
        self.text1.set("What is your name?")

        self.inputText1 = tkinter.Text(
            self.frame,
            width=30,
            height=1,
            bg="light yellow"
        )
        self.inputText1.pack()

        self.btn1 = tkinter.Button(
            self.frame, 
            width=30,
            text="Next",
            command=self.registerFace2
        ).pack()

     

    def registerFace2(self):        
        self.saveName()
        for widgets in self.window.winfo_children():
            widgets.destroy()
        
        self.frame = tkinter.Frame(self.window).pack(side="top")
        
        self.tmpCav1 = tkinter.Canvas(
            self.frame, 
            height=50,
            width=1
        ).pack()

        
        self.text1 = tkinter.StringVar()
        self.labelName = tkinter.Label(
            self.frame,
            textvariable=self.text1,
            font=("Helvetica", 19)
        )

        self.labelName.pack()
        self.text1.set("Take a photo of yourself")

         # Display camera
        self.cav2 = tkinter.Canvas(
            self.frame,
            width = self.vid.width,
            height=self.vid.height
        )
        self.cav2.pack()
        self.btn1 = tkinter.Button(
            self.frame, 
            width=30,
            text="Capture",
            command=self.snapshot
        ).pack()


        self.delay = 15
        self.update2()

    def detectFace(self):
        print("detectFace")
        for widgets in self.window.winfo_children():
            widgets.destroy()
        self.frame = tkinter.Frame(self.window).pack(side="top")

        # Display camera 
        self.cav2 = tkinter.Canvas(
            self.frame,
            width=self.vid.width,
            height=self.vid.height
        )
        self.cav2.pack()


        self.text1 = tkinter.StringVar()
        # Display name of face detected
        self.labelName = tkinter.Label(
            self.frame,
            textvariable=self.text1,
            font=("Helvetica", 30)
        ).pack()

        self.text2 = tkinter.StringVar()
        self.labelName2 = tkinter.Label(
            self.frame,
            textvariable=self.text2,
            font=("Helvetica", 19)
            ).pack()

        self.delay = 15
        self.update()

    def saveName(self):
        self.save_name = self.inputText1.get(1.0, "end-1c")
        print(self.save_name)

    def snapshot(self):
        temp = list(self.save_name)
        self.fullName = ""
        for i in temp:
            if i == " ":
                i = "_"
            self.fullName += i
        
        #Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("images/" + self.fullName + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
        # Update screen
        for widgets in self.window.winfo_children():
            widgets.destroy()
        self.frame = tkinter.Frame(self.window).pack()
        
        self.tmpCav1 = tkinter.Canvas(
            self.frame, 
            height=300
        ).pack()

        self.text1 = tkinter.StringVar()
        self.labelName = tkinter.Label(
            self.frame,
            textvariable=self.text1,
            font=("Helvetica", 19)
        )

        self.labelName.pack()
        
        self.text1.set("User Registered successfully")

        self.btn1 = tkinter.Button(
            self.frame, 
            width=30,
            text="Go back to main menu",
            command=self.menuScreen,
        ).pack()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.cav2.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.cav2.create_rectangle(
                self.vid.x1, self.vid.y1, 
                self.vid.x2, self.vid.y2,
                outline="green",
                width=4
                )
        self.text1.set(self.vid.getDisplayName())
        self.text2.set(self.vid.getDisplaySuccess())




        # print("I'm in update 1")
        self.window.after(self.delay, self.update)

    def update2(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.cav2.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        # print("I'm in update 2")
        self.window.after(self.delay, self.update2)



class MyVideoCapture:
    __myDisplayName = ""
    __successText = ""
    
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.y1, self.x2, self.y2, self.x1 = (0,0,0,0)

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
                name = classNames[matchIndex]
                nameList = list(name)
                nameList[0] = nameList[0].upper()
                name = ''.join(nameList)
                #print(name)
                self.y1, self.x2, self.y2, self.x1 = faceLoc
                self.y1, self.x2, self.y2, self.x1 = self.y1*4,self.x2*4,self.y2*4,self.x1*4
                # cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                # cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                # cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                
                newName = ""
                for i in name:
                    if i == "_":
                        i = " "
                    newName += i
                
                markAttendance(newName)
                self.setDisplayName(newName)
                self.setSuccessText("Login Successful")
            else:
                self.setDisplayName(" ")
                self.setSuccessText("No face detected")
        #=============================
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)


    def get_frame2(self):
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
                name = classNames[matchIndex]
                nameList = list(name)
                nameList[0] = nameList[0].upper()
                name = ''.join(nameList)
                #print(name)
                self.y1, self.x2, self.y2, self.x1 = faceLoc
                self.y1, self.x2, self.y2, self.x1 = self.y1*4,self.x2*4,self.y2*4,self.x1*4
                # cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                # cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                # cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        #=============================
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)


    def setDisplayName(self, text):
        self.__myDisplayName = text 
    
    def setSuccessText(self, text):
        self.__successText = text
    
    def getDisplayName(self):
        return self.__myDisplayName

    def getDisplaySuccess(self):
        return self.__successText

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
mainApp = App(tkinter.Tk(), "Tkinter and OpenCV")
