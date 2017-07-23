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
    
    print ("Press key `p` to pause the video to start tracking")
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        if not retval:
            print ("Cannot capture frame device")
            exit()
        if(cv2.waitKey(10)==ord('p')):
            break
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
    cv2.destroyWindow("Image")

    # Co-ordinates of objects to be tracked 
    # will be stored in a list named `points`
    points = get_points.run(img, multi=True) 
    print(points)
    if not points:
        print ("ERROR: No object to be tracked.")
        exit()

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)

    # Initial co-ordinates of the object to be tracked 
    # Create the tracker object
    tracker = [dlib.correlation_tracker() for _ in range(len(points))]
    # Provide the tracker the initial position of the object
    [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points)]
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 9999)
    print (sys.stderr, 'connecting to %s port %s' % server_address)
    sock.connect(server_address)
    file=open('coordinate.txt', 'w')
    while True:
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print ("Cannot capture frame device | CODE TERMINATION :( ")
            exit()
        # Update the tracker  
        start=time.time()
        for i in range(len(tracker)):
            tracker[i].update(img)
            # Get the position of th object, draw a 
            # bounding box around it and display it.
            rect = tracker[i].get_position()
            pt1 = (int(rect.left()), int(rect.top()))
            pt2 = (int(rect.right()), int(rect.bottom()))
            if not (pt1[0]<0 or pt1[1]<0 or pt2[0]<0 or pt2[1]<0):
               cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
               print ("Object {} tracked at [{}, {}] \r".format(i, pt1, pt2))
               a=str(int(rect.left()))
               b=str(int(rect.top()))
               c=str(int(rect.right()))
               d=str(int(rect.bottom()))
               value=(a+" "+b+" "+c+" "+d)
               file.write(value+"\n")
               sock.sendall(value.encode('utf-8'))
               if dispLoc:
                   loc = (int(rect.left()), int(rect.top()-20))
                   txt = "Object tracked at [{}, {}]".format(pt1, pt2)
                   cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        end=time.time()
        ##print frames/second here
        #print("fps: ",(1/(end-start)))
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object
    file.close()
    sock.close()
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
