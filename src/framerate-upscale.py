import sys
import cv2
import numpy as np

if __name__ == '__main__':

    # Get input and output arguments
    args = sys.argv
    if len(args) not in (3,4):
        print("Invalid arguments given. Usage: input-video-filepath output-video-filepath [optional -s to play output]")
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
    nFrames = int(vidFile.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Number of frames in original video: {nFrames}')
    fps = vidFile.get(cv2.CAP_PROP_FPS)
    frame_time = int((1/fps) * 1000) # Frame time in milliseconds
    print(f'Frame rate of orginal video: {fps}')
    dimensions = (int(vidFile.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(vidFile.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(f'Dimensions of video: {dimensions}')

    # Read frames of input video
    frames = []
    for i in range(nFrames):
        ret, frame = vidFile.read()
        frames.append(frame)
    vidFile.release()
    
    # Create new frames by averaging colours of two neighbouring frames
    new_frames = []
    frame_stack = np.zeros(shape=(2, dimensions[0], dimensions[1], 3), dtype=np.uint8)
    for i in range(len(frames)-1):
        frame_stack[0] = frames[i]
        frame_stack[1] = frames[i+1]
        frame_average = np.average(frame_stack, axis=0).astype(np.uint8)
        new_frames.append(frame_average)
    
    # Gather old and new frames together
    out_frames = []
    for i in range(nFrames-1):
        out_frames.append(frames[i])
        out_frames.append(new_frames[i])
    out_frames.append(frames[len(frames)-1])

    # Create output file 
    output = cv2.VideoWriter(args[2],cv2.VideoWriter_fourcc('M','P','E','G'), fps*2, (dimensions[1],dimensions[0]))
    for frame in out_frames:
        output.write(frame)
    output.release()

    # If requested, playback video
    if len(args) == 4 and args[3] == '-s':
        for frame in out_frames:
            # Show frame
            cv2.imshow('frame',frame)

            # Press Q on keyboard to stop playback
            if cv2.waitKey(frame_time) & 0xFF == ord('q'):
                break

