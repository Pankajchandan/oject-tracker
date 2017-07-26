# Import the required modules
import dlib
import cv2
import argparse as ap
import get_points
import time
import socket
import sys
import numpy as np

def run(source=0, dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print ("Video device or file couldn't be opened")
        exit()
    
    # Create a TCP/IP socket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    #server_address = ('localhost', 9999)
    #print (sys.stderr, 'connecting to %s port %s' % server_address)
    #sock.connect(server_address)
    #file=open('coordinate.txt', 'w')
    file=open('/home/nvidia/darknet/test.txt','r')
    label=["Mock", "Car", "SUV", "SmallTruck", "MediumTruck", "LargeTruck", "Pedestrian", "Bus", "Van", "GroupOfPeople", "Bicycle", "Motorcycle"
            , "TrafficSignal-Green", "TrafficSignal-Yellow", "TrafficSignal-Red"]
    while True:
        points=list()
        while True:
            point=file.readline()
            if point=='eoframe\n':
                break
            if point=='':
                points=lastpoints
                break
            points.append(point)
        # Read frame from device or file
        lastpoints=points
        retval, img = cam.read()
        if not retval:
            print ("Cannot capture frame device | CODE TERMINATION :( ")
            exit() 
        start=time.time()
        for i,coord in enumerate(points):
            start_track_time=time.time()
            obj=coord.split()
            # Get the position of th object, draw a 
            # bounding box around it and display it.
            #rect = tracker[i].get_position()
            end_track_time=time.time()
            print("object track time : ",end_track_time-start_track_time)
            pt1 = (int(obj[1]), int(obj[2]))
            pt2 = (int(obj[3]), int(obj[4]))
            if not (pt1[0]<0 or pt1[1]<0 or pt2[0]<0 or pt2[1]<0):
               ##draw here
               start_draw_time=time.time()
               cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
               cv2.putText(img,label[int(obj[0])],(int(obj[1]), (int(obj[2])-10)), cv2.FONT_HERSHEY_SIMPLEX , 0.5,(255,255,255),2,cv2.LINE_AA)
               end_draw_time=time.time()
               print("box draw time : ",end_draw_time-start_draw_time)
               print ("Object {} tracked at [{}, {}] \r".format(i, pt1, pt2))
               a=str(int(obj[1]))
               b=str(int(obj[2]))
               c=str(int(obj[3]))
               d=str(int(obj[4]))
               value=(a+" "+b+" "+c+" "+d)
               #file.write(value+"\n")
               #sock.sendall(value.encode('utf-8'))
               if dispLoc:
                   loc = (int(rect.left()), int(rect.top()-20))
                   txt = "Object tracked at [{}, {}]".format(pt1, pt2)
                   cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        end=time.time()
        ##print frames/second here
        print("fps: ",(1/(end-start)))
        start_disp_time=time.time()
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        end_disp_time=time.time()
        print("image disp time : ",end_disp_time-start_disp_time)
        print("\n \n")
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object
    file.close()
    #sock.close()
    cam.release()

if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    run(source, args["dispLoc"])
