import cv2
Frame = ''
     
def initialFrameCreation(file_path):
      
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error opening video file:", file_path)
        exit()

    ret, frame = cap.read()

    current_frame = 1

    if not ret:
        print("Error reading video frame")
        exit()

    else:
        
        name = './' +'Frame_' + str(current_frame)+ '.jpg'
        cv2.imwrite(name, frame)
        Frame = 'Frame_' + str(current_frame)

    cap.release()
    cv2.destroyAllWindows()
    return Frame


# print(initialFrameCreation('video7.avi'))

        