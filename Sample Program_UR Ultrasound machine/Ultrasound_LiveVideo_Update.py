#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
#import sys
from tkinter import *
import tkinter
import cv2
import PIL
import PIL.Image, PIL.ImageTk
import time
import multiprocessing
import os
from time import sleep
from multiprocessing import Value, Lock
from ctypes import c_int
from threading import Thread

##GPIO.setmode(GPIO.BOARD)

##ControlPin = [7,11,13,15]
##
##for pin in ControlPin:
##    GPIO.setup(pin,GPIO.OUT)
##    GPIO.output(pin,0)
##
##    seq= [[1,0,0,0],
##          [1,1,0,0],
##          [0,1,0,0],
##          [0,1,1,0],
##          [0,0,1,0],
##          [0,0,1,1],
##          [0,0,0,1],
##          [1,0,0,1]]
DIR = 20  # Direction GPIO
STEP = 21 # Step GPIO Pin
CW = 1    # Clockwise Rotation
CCW = 0   # Counterclockwise Rotation
SPR = 200 # Steps per Revolution (360/1.8)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
#GPIO.output(DIR,CW)

MODE = (14, 15, 18)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0,0,0),
              'Half': (1,0,0),
              '1/4': (0,1,0),
              '1/8': (1,1,0),
              '1/16': (1,1,1)}
GPIO.output(MODE, RESOLUTION['1/16'])

#step_count = SPR * 2
delay = 0.005

counter = Value(c_int)
counter_lock = Lock()

e = multiprocessing.Event()
p = None    

class App:

    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        
        # open video source
        self.vid = MyVideoCapture(self.video_source)
        
        #Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height= self.vid.height)
        self.canvas.pack()
        button1 = Button(window, text= "Axial Scan", command=self.move_forward)
        button2 = Button(window, text="Move Back to Start", command=self.vid.move_backward)
        #Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", command=self.snapshot)#width=50
        button3 = Button(window, text="Move Back to Start", command=self.reset)
        button4 = Button(window, text="Done", command=self.close_window)
        
        start_vid_button = tkinter.Button(window, text='Record Video',command=self.vid.short_vid)
        #stSagButton = tkinter.Button(window, text='Sagittal Scan',command=self.vid.start_recording_proc_short)
        startbutton = tkinter.Button(window, text='Axial Scan',command=self.vid.move_forward_vid)
        stSagButton = tkinter.Button(window, text='Sagittal Scan',command=self.vid.move_short_vid)
        stopbutton = tkinter.Button(window, text='STOP RECORDING',command=self.vid.stoprecording)
        sagittalbutton = tkinter.Button(window, text='Sagittal Scan',command=self.move_short)

##        New_scan = tkinter.Button(window, text='New Scan', command=self.new_scan)
##        
##        New_scan.pack()
##        button1.pack()
##        button3.pack()
##        self.btn_snapshot.pack()#anchor=tkinter.CENTER, expand=True)
##        sagittalbutton.pack()
        startbutton.pack()
        start_vid_button.pack()
#        stSagButton.pack()
        button2.pack()
        
##        stopbutton.pack()
        button4.pack()
                
        directory = "Patient Data"
        os.chdir(directory)
        patient_num = len(os.listdir('/home/pi/Desktop/Patient Data'))
        new_patient = 'Patient'+ str(patient_num)
        os.mkdir(new_patient)
        os.chdir(new_patient)

        #After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
    

        
        self.window.mainloop()
        
##    def new_scan(self):
##        directory = "Patient Data"
##        os.chdir(directory)
##        scan_num = len(os.listdir('/home/pi/Desktop/Patient Data'))
##        new_scan = 'Scan'+ str(scan_num)
##        os.mkdir(new_scan)
##        os.chdir(new_scan)
##       
        
        
    def move_forward(self):
##        new_scan = 'New_Scan'
##        os.mkdir(new_scan)
##        os.chdir(new_scan)
        #global CW,DIR,STEP,SPR,delay
    #for num in range(40):
##        for i in range(17500):
##            for halfstep in range(7,-1,-1):
##            #for fullstep in range(4):
##                for pin in range(4):
##                    #for_count = for_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##        time.sleep(1)
##        self.snapshot()
        GPIO.output(DIR,CW)
        step_count = SPR *7*16
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        self.count_full()
        global count
        print(count)
        

    def move_backward(self):
##        for i in range(17500):
##            for halfstep in range(8):
##             #for fullstep in range(4):
##                 for pin in range(4):
##                    #back_count = back_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##        time.sleep(0.5)
##        self.snapshot()
        GPIO.output(DIR,CCW)
        step_count = SPR *1
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        self.count_rev()
        global count
        print(count)
        
    def move_short(self):
##        for i in range(6863):
##            for halfstep in range(8):
##             #for fullstep in range(4):
##                 for pin in range(4):
##                    #back_count = back_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##        time.sleep(0.5)
##        self.snapshot()
        GPIO.output(DIR,CW)
        step_count = SPR *2
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        self.count()
        global count
        print(count)
        
    def close_window(self):
        GPIO.cleanup()
        os.chdir('/home/pi/Desktop')
        exit()
        window.quit()
        window.destroy()

    def reset(self):
        #scan_num = len(os.listdir('/home/pi/Desktop/Patient Data/Patient'+str(patient_num)))
        new_scan = 'New_Scan'
        os.mkdir(new_scan)
        os.chdir(new_scan)
        distance = abs(int(count)*14)
        if count>0:
            for i in range(distance):
                for halfstep in range(8):
                #for fullstep in range(4):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin],seq[halfstep][pin])
                        #GPIO.output(ControlPin[pin],seq[fullstep][pin])
                        time.sleep(0.001)
                        
        else:
            for i in range(distance):
                for halfstep in range(7,-1,-1):
                #for fullstep in range(4):
                    for pin in range(4):
                        GPIO.output(ControlPin[pin],seq[halfstep][pin])
                        #GPIO.output(ControlPin[pin],seq[fullstep][pin])
                        time.sleep(0.001)

    def snapshot(self):
        ret, frame = self.vid.get_frame()

    
        if ret:
            cv2.imwrite("frame-" + time.strftime("%m-%d-%Y-%H-%M-%S") + ".tif", frame[20:416,90:613])#cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
            
    
    def update(self):
        #Get a frame from the video source
        ret, frame = self.vid.get_frame()
        
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image = self.photo,anchor = tkinter.N)
        
        self.window.after(self.delay, self.update)
##   
##    def count(self):
##        global count
##        count += 20
##    def count_rev(self):
##        global count
##        count -= 10
##    def count_full(self):
##        global count
##        count += 70
##    
##    def startrecording(self,e,video_source=0):
##
##        #self.cap = cv2.VideoCapture(video_source)
##        self.out = cv2.VideoWriter("output.avi",cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (640,480))
##        
##        while (self.vid.isOpened()):
##            print("I'm in")
##            if e.is_set():
##                print("I'm out")
##                self.cap.release()
##                self.out.release()
##                #cv2.destroyAllWindows()
##                e.clear()
##            ret, frame = self.cap.read()
##            print("here")
##            if ret:
##                print("I'm really in")
##                #frame = cv2.flip(frame,0)
##                self.out.write(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB).astype('uint8'))
##            else:
##                print("why?")
##                break
##            
##    def start_recording_proc(self,video_source=0):
##        global p
##        p = multiprocessing.Process(target=self.startrecording, args=(e,video_source,))
##        p.start()
##    
#### end Video Capture 
##    def stoprecording(self):
##        e.set()
##        p.join()
        
        
      
        
class MyVideoCapture: 
    
    def __init__(self, video_source=0):
        #open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
    
        #Get video source width and hieght
        self.width = (.5*self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = (.5*self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(self.height)
        print(self.width)
        
        
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            #print('Here')
            if ret:
                #print('there')
                #Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
                
            else:
                print('empty')
                return (ret, None)
            
        else:
            print('wrong')
            return (ret, None)
        
     
      
    #Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            
    def start_recording_proc(self,video_source=0):
        global p
        p = multiprocessing.Process(target=self.startrecording, args=(e,video_source,))
        p.start()
    
    def startrecording(self,e,video_source=0):

        #self.cap = cv2.VideoCapture(video_source)
        self.out = cv2.VideoWriter("Video-" + time.strftime("%m-%d-%Y-%H-%M-%S") + ".avi",cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (640,480))
        
        while (self.vid.isOpened()):
            #print("I'm in")
            if e.is_set():
                #print("I'm out")
                self.vid.release()
                self.out.release()
                #cv2.destroyAllWindows()
                e.clear()
            #for num in range(SPR):
            ret, frame = self.vid.read()
            #print("here")
            if ret==True:
                #print("I'm really in")
                #frame = cv2.flip(frame,0)
                #self.out.write(frame)#cv2.cvtColor(frame,cv2.COLOR_BGR2RGB).astype('uint8')
                
                self.out.write(frame)#[20:416,90:613])#cv2.cvtColor(frame,cv2.COLOR_BGR2RGB).astype('uint8')
                #self.move_forward()
                
            else:
                #print("why?")
                break
            #e.set()
            #p.join
    ## end Video Capture
    def start_recording_proc_short(self,video_source=0):
        global p
        p = multiprocessing.Process(target=self.startrecording_short, args=(e,video_source,))
        p.start()
    
    def startrecording_short(self,e,video_source=0):

        #self.cap = cv2.VideoCapture(video_source)
        self.out = cv2.VideoWriter("Video-" + time.strftime("%m-%d-%Y-%H-%M-%S") + ".avi",cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (640,480))
        
        while (self.vid.isOpened()):
            #print("I'm in")
            if e.is_set():
                #print("I'm out")
                self.vid.release()
                self.out.release()
                #cv2.destroyAllWindows()
                e.clear()
            ret, frame = self.vid.read()
            #print("here")
            if ret==True:
                #print("I'm really in")
                #frame = cv2.flip(frame,0)
                #self.out.write(frame)#cv2.cvtColor(frame,cv2.COLOR_BGR2RGB).astype('uint8')
                self.out.write(frame)#[20:416,90:613])#cv2.cvtColor(frame,cv2.COLOR_BGR2RGB).astype('uint8')
                #self.move_short()
                
            else:
                #print("why?")
                
                break
            #e.set()  
            #p.join()
            
    ## end Video Capture 
    def stoprecording(self):
        e.set()
        p.join()
    
##    def move_backward(self):
##        for i in range(17500):
##            for halfstep in range(8):
##             #for fullstep in range(4):
##                 for pin in range(4):
##                    #back_count = back_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##    def move_short(self):
##        for i in range(6863):
##            for halfstep in range(8):
##             #for fullstep in range(4):
##                 for pin in range(4):
##                    #back_count = back_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
    def move_forward_vid(self):
        if counter.value == 0:
##        new_scan = 'New_Scan'
##        os.mkdir(new_scan)
##        os.chdir(new_scan)
        #global CW,DIR,STEP,SPR,delay
    #for num in range(40):
##        for i in range(17500):
##            for halfstep in range(7,-1,-1):
##            #for fullstep in range(4):
##                for pin in range(4):
##                    #for_count = for_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##        time.sleep(1)
##        self.snapshot()
            self.start_recording_proc(video_source=0)
            GPIO.output(DIR,CW)
            step_count = SPR *17
            for x in range(step_count):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)
            self.count_full()
            self.stoprecording()
            #global count1,count2,count3
            print(counter.value)
    
    def move_short_vid(self):
        if counter.value <=5:
##        for i in range(6863):
##            for halfstep in range(8):
##             #for fullstep in range(4):
##                 for pin in range(4):
##                    #back_count = back_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##        time.sleep(0.5)
##        self.snapshot()
            self.start_recording_proc_short(video_source=0)
            GPIO.output(DIR,CW)
            step_count = SPR *7
            for x in range(step_count):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)
            self.count()
            self.stoprecording()
            #global count1,count2,count3
            print(counter.value)
        
    
    def move_backward(self):
##        for i in range(17500):
##            for halfstep in range(8):
##             #for fullstep in range(4):
##                 for pin in range(4):
##                    #back_count = back_count+1
##                    GPIO.output(ControlPin[pin],seq[halfstep][pin])
##                    #GPIO.output(ControlPin[pin],seq[fullstep][pin])
##                    time.sleep(0.00015)
##        time.sleep(0.5)
##        self.snapshot()
        GPIO.output(DIR,CCW)
        step_count = SPR*counter.value
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        self.count_rev()
        #global count1,count2,count3
        print(counter.value)
    
    def short_vid(self):
        self.start_recording_proc(video_source=0)
        tally = 0 
        while tally < 5:
            sleep(1)
            tally += 1
        self.stoprecording()
        

    
    def count(self):
        with counter_lock:
            counter.value += 2
        
        
    def count_rev(self):
        with counter_lock:
            counter.value -= counter.value
        
        
    def count_full(self):
        with counter_lock:
            counter.value += 17
        
        
    
#Create a window and pass it to the Application object
App(tkinter.Tk(), "Ultrasound Device Control")

