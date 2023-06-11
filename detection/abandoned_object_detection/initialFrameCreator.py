import cv2

def extract_first_frame(video_file, frame_file):
    # Open the video file for reading
    cam = cv2.VideoCapture(video_file)

    # Read the first frame of the video
    ret, frame = cam.read()

    # If the frame was successfully read
    if ret:

        # Save the first frame as a JPEG image file
        cv2.imwrite(frame_file, frame)

    # Release the video file and destroy all windows
    cam.release()
    cv2.destroyAllWindows()

