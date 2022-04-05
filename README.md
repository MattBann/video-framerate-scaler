# video-framerate-scaler

A simple tool for upscaling or downscaling the framerate of a video.

## Requirements

- Python 3
- OpenCV python
- numpy

## Usage

To upscale the framerate of a video to twice its original framerate, run framerate-upscale.py with two arguments, the filepath of the input video, and the filepath for where you want the output to go. Add -s on the end to play the video once finished.  
To downscale the framerate of a video to half its orignal framerate, run framerate-downscale.py with two arguments, the filepath of the input video, and the filepath for where you want the output to go.

For example:

    python src/framerate-upscale.py video.mp4 output.mp4 -s

## How it works

The downscaler works by omitting half the frames of the video, then saving the video with half the frame rate.  
The upscaler creates new frames from the average colours of two frames, then inserts the new frame inbetween, then saves the video with double the frame rate.
