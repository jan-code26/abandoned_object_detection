import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import numpy as np
from abandone_object_detection import settings
from detection.abandoned_object_detection.Abandoned_object_detection import detect_object
from detection.abandoned_object_detection.tracker import ObjectTracker
import detection.abandoned_object_detection.FrameCreation as fc
from moviepy.editor import VideoFileClip
from django.http import FileResponse, HttpResponse
from django.core.files.storage import default_storage
import cv2
from django.core.files import File
from .models import DetectionResult, DetectionVideo
from django.db import models


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
            return render(request, 'login.html')
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
            
            return redirect('upload_video')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']        
        new_entry = DetectionVideo()
        new_entry.video_file.save(video_file.name, video_file)

        video_path = new_entry.video_file.path
        detect_object(video_path)
        return HttpResponse('Video uploaded successfully')
    
    return render(request, 'upload_video.html')

def base(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']        
        new_entry = DetectionVideo()
        new_entry.video_file.save(video_file.name, video_file)

        video_path = new_entry.video_file.path
        detect_object(video_path)
        return HttpResponse('Video uploaded successfully')
    
    return render(request, 'abandoned_object_detection.html')

def documentation(request):
    return render(request, 'doc.html')