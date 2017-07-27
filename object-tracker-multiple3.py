# Import the required modules
import dlib
import cv2
import argparse as ap
import get_points
import time
import socket
import sys

def run(source=0, dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print ("Video device or file couldn't be opened")
        exit()
    
    counter=0
    while True:
       img=cam.read()
       if counter==3:
           break
       counter+=1

    file=open('/home/nvidia/darknet/test.txt','r')

    #label=["Mock", "Car", "SUV", "SmallTruck", "MediumTruck", "LargeTruck", "Pedestrian", "Bus", "Van", "GroupOfPeople", "Bicycle", "Motorcycle"
            #, "TrafficSignal-Green", "TrafficSignal-Yellow", "TrafficSignal-Red"]
    
    points=list()
    counter=0
    while counter<4:
        point=file.readline()
        if point=='eoframe\n':
            counter+=1
            continue
        if counter==3:
            points.append(point)
    file.close()
    print(points)
    # Initial co-ordinates of the object to be tracked 
    # Create the tracker object
    tracker = [dlib.correlation_tracker() for _ in range(len(points))]
    # Provide the tracker the initial position of the object
    [tracker[i].start_track(img, dlib.rectangle(int(rect[2]),int(rect[4]),int(rect[6]),int(rect[8]))) for i, rect in enumerate(points)]
 
    while True:
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print ("Cannot capture frame device | CODE TERMINATION :( ")
            exit()
        # Update the tracker  
        start=time.time()
        for i in range(len(tracker)):
            start_track_time=time.time()
            tracker[i].update(img)
            # Get the position of th object, draw a 
            # bounding box around it and display it.
            rect = tracker[i].get_position()
            end_track_time=time.time()
            print("object track time : ",end_track_time-start_track_time)
            pt1 = (int(rect.left()), int(rect.top()))
            pt2 = (int(rect.right()), int(rect.bottom()))
            if not (pt1[0]<0 or pt1[1]<0 or pt2[0]<0 or pt2[1]<0):
               ##draw here
               start_draw_time=time.time()
               cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
               end_draw_time=time.time()
               print("box draw time : ",end_draw_time-start_draw_time)
               print ("Object {} tracked at [{}, {}] \r".format(i, pt1, pt2))
               a=str(int(rect.left()))
               b=str(int(rect.top()))
               c=str(int(rect.right()))
               d=str(int(rect.bottom()))
               value=(a+" "+b+" "+c+" "+d)
               file.write(value+"\n")
               #sock.sendall(value.encode('utf-8'))
               if dispLoc:
                   loc = (int(rect.left()), int(rect.top()-20))
                   txt = "Object tracked at [{}, {}]".format(pt1, pt2)
                   cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        end=time.time()
        ##print frames/second here
        #print("fps: ",(1/(end-start)))
        start_disp_time=time.time()
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        end_disp_time=time.time()
        #print("image disp time : ",end_disp_time-start_disp_time)
        #print("\n \n")
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object
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
