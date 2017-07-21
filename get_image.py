# Import the required modules
import pickle
import cv2
import argparse as ap
import get_points

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
    points = get_points.run(img) 

    if not points:
        print ("ERROR: No object to be tracked.")
        exit()
    
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)
    
    imglist=[img,points]
    pickle.dump( imglist, open( "save.p", "wb" ) )

    if cv2.waitKey(1) == 27:
        cam.release() 
        cv.destroyAllWindows()

    
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
