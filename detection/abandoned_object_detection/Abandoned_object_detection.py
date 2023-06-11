import os
# import winsound

import numpy as np
import cv2
import detection.abandoned_object_detection.FrameCreation as fc

from detection.abandoned_object_detection.tracker import ObjectTracker



def detect_object():
    try:	
        if not os.path.exists('output'):
            os.makedirs('output')
    except OSError:
        print ('Error: Creating directory of output')

    op =  1 
    det = 1

    tracker = ObjectTracker()

    file_path = '/Users/jahnavipatel/abandone_object_detection/detection/abandoned_object_detection/video7.avi'


    firstframe_path = fc.initialFrameCreation(file_path)+'.jpg'


    firstframe = cv2.imread(firstframe_path)

    firstframe_gray = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
    firstframe_blur = cv2.GaussianBlur(firstframe_gray,(3,3),0)


    cap = cv2.VideoCapture(file_path)
    AbandonedObjectLT = set()

    while (cap.isOpened()):
        ret, frame = cap.read()
    
        frame_height, frame_width, _ = frame.shape

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray,(3,3),0)

        frame_diff = cv2.absdiff(firstframe_blur, frame_blur)
    
        edged = cv2.Canny(frame_diff,10,200) 
    
        kernel = np.ones((2,2),np.uint8)
        thresh = cv2.morphologyEx(edged,cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        detections=[]
        count = 0
        for c in cnts:
            contourArea = cv2.contourArea(c)
            
            if contourArea > 200 and contourArea < 20000:
                count +=1

                (x, y, w, h) = cv2.boundingRect(c)

                detections.append([x, y, w, h])

        _, abandoned_objects = tracker.update(detections)
        
        firstTime = False   

        for objects in abandoned_objects:
            _, x2, y2, w2, h2, _ = objects

            if tuple(objects[1:-1]) not in AbandonedObjectLT:
                firstTime = True
                AbandonedObjectLT.add(tuple(objects[1:-1]))
            cv2.putText(frame, "Suspicious object detected", (x2, y2 - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)
            cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
            det_frame = frame[y2:y2+h2,x2:x2+w2]
            det_name = './det/det' + str(det) + '.jpg'
            cv2.imwrite(det_name, det_frame)
            det+=1

        cv2.imshow('main',frame)
        
        if(len(abandoned_objects)!= 0 and firstTime):
            print(abandoned_objects)
            # winsound.Beep(2000,1)
            name = './output/op' + str(op) + '.jpg'
            cv2.imwrite(name, frame)
            op+=1

        if cv2.waitKey(15) == ord('q'):
            break
        

    cv2.destroyAllWindows()



