import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
import cv2
import os
import sqlite3
from datetime import date
from .models import Data
from django.contrib import messages

def home(request):
    if request.method == 'POST' and 'take attendance' in request.POST:
        
        output_dir = os.path.join('daily_attendance', str(date.today()))
        os.makedirs(output_dir, exist_ok=True)

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image_count = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (225, 0, 0), 2)
                    face_image = gray[y:y+h, x:x+w]
                    image_path = os.path.join(output_dir, f'image_{image_count}.jpg')
                    cv2.imwrite(image_path, face_image)
                    image_count += 1

                cv2.imshow('capture_face', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

    
    return render(request, 'home.html')


def login(request):
        return render(request,'login.html')
   
def take_images(request):
    output_dir = 'captured_images/'
    os.makedirs(output_dir, exist_ok=True)

    if request.method == 'GET':
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image_count = 0

        if 'take_image' in request.GET:
            try:
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (225, 0, 0), 2)
                        face_image = gray[y:y+h, x:x+w]
                        image_path = os.path.join(output_dir, f'image_{image_count}.jpg')
                        cv2.imwrite(image_path, face_image)
                        image_count += 1

                    cv2.imshow('capture_face', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            finally:
                cap.release()
                cv2.destroyAllWindows()

        if 'save_profile' in request.GET:
            cv2.destroyAllWindows()
            cap.release()
            return render(request, 'Take_image.html')

    return render(request, 'Take_image.html')

def get_profile_count():
    with sqlite3.connect('attendance.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Students")
        profile_count = cursor.fetchone()[0]
    return profile_count









