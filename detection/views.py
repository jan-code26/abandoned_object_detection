import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import numpy as np
from abandone_object_detection import settings
from detection.abandoned_object_detection.tracker import ObjectTracker
import detection.abandoned_object_detection.FrameCreation as fc
from moviepy.editor import VideoFileClip
from django.http import FileResponse
import cv2


def abandoned_object_detection(request):
    if request.method == 'POST':
        detect_object()
        # perform abandoned object detection on the video
        # and save the output
        return render(request, 'abandoned_object_detection/detect_object.html')
    else:
        return render(request, 'upload_video.html')
    
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': 'Username already exists'})
            
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            
            # Log in the user and redirect to the homepage
            login(request, user)
            return render(request, 'upload_video.html')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Log in the user and redirect to the homepage
            login(request, user)    
            # return redirect('detect/')
            return render(request, 'upload_video.html')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        
        # Save the video file or perform any desired processing
        
        # Assuming the video is saved to a 'media' directory
        video_url = '/Users/jahnavipatel/abandone_object_detection/detection/abandoned_object_detection/video7.avi'
        
        # Pass the video URL to the success page
        return render(request, 'success.html', {'video_url': video_url})
    
    return render(request, 'upload_video.html')


def play_avi(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        # video_path = save_video_file(video_file)  # Save the video file to a specific location
        avi_file_path = '/Users/jahnavipatel/abandone_object_detection/detection/abandoned_object_detection/' + str(video_file)
        print(avi_file_path + "bshjxabds")
        detect_object(avi_file_path)
        # Return the video file as a response
        return FileResponse(open(avi_file_path, 'rb'), content_type='video/x-msvideo')
    
    return render(request, 'upload_form.html')



def upload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        video_path = os.path.join(settings.MEDIA_ROOT, 'video.mp4')
        with open(video_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        results = detect_object(video_path)
        context = {'results': results}
        return render(request, 'result.html', context)
    else:
        return render(request, 'index.html')

def detect_object(file_path):
    try:
        if not os.path.exists('output'):
            os.makedirs('output')
    except OSError:
        print('Error: Creating directory of output')

    op = 1
    det = 1

    tracker = ObjectTracker()
    print(file_path + " jhbjhb")
    firstframe_path = fc.initialFrameCreation(file_path) + '.jpg'
    firstframe = cv2.imread(firstframe_path)
    firstframe_gray = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
    firstframe_blur = cv2.GaussianBlur(firstframe_gray, (3, 3), 0)

    cap = cv2.VideoCapture(file_path)
    AbandonedObjectLT = set()
    results = []

    while (cap.isOpened()):
        ret, frame = cap.read()

        frame_height, frame_width, _ = frame.shape

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_blur = cv2.GaussianBlur(frame_gray, (3, 3), 0)

        frame_diff = cv2.absdiff(firstframe_blur, frame_blur)

        edged = cv2.Canny(frame_diff, 10, 200)

        kernel = np.ones((2, 2), np.uint8)
        thresh = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        count = 0
        for c in cnts:
            contourArea = cv2.contourArea(c)

            if contourArea > 200 and contourArea < 20000:
                count += 1

                (x, y, w, h) = cv2.boundingRect(c)

                detections.append([x, y, w, h])

        _, abandoned_objects = tracker.update(detections)

        firstTime = False

        for objects in abandoned_objects:
            _, x2, y2, w2, h2, _ = objects

            if tuple(objects[1:-1]) not in AbandonedObjectLT:
                firstTime = True
                AbandonedObjectLT.add(tuple(objects[1:-1]))
            cv2.putText(frame, "Suspicious object detected", (x2, y2 - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255),
                        2)
            cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)
            det_frame = frame[y2:y2 + h2, x2:x2 + w2]
            det_name = './det/det' + str(det) + '.jpg'
            cv2.imwrite(det_name, det_frame)
            det += 1

        if len(abandoned_objects) != 0 and firstTime:
            results.append(abandoned_objects)
            name = './output/op' + str(op) + '.jpg'
            cv2.imwrite(name, frame)
            op += 1

        if cv2.waitKey(15) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return results