import cv2
import sys

if __name__ == '__main__':

    # Get input and output arguments
    args = sys.argv
    if len(args) != 2:
        print("Invalid arguments given. Usage: input-video-filepath output-video-filepath")
        sys.exit(1)

    # Attempt to open input video
    try:
        vidFile = cv2.VideoCapture(args[1])
    except:
        print("Problem opening input stream")
        sys.exit(1)
    if not vidFile.isOpened():
        print("Capture stream not open")
        sys.exit(1)
    
    # Get relevant metadata
    fps = int(vidFile.get(cv2.CAP_PROP_FPS))
    dimensions = (int(vidFile.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vidFile.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    nFrames = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create output file
    output = cv2.VideoWriter(args[2],cv2.VideoWriter_fourcc('M','P','E','G'), fps//2, dimensions)
    for i in range(nFrames//2):
        # Remove half the frames by read twice, write once
        ret, frame = vidFile.read()
        ret, frame = vidFile.read()
        output.write(frame)
    
    vidFile.release()
    output.release()