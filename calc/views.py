from django.shortcuts import render
from django.http import HttpResponse
import cv2
import os
import sqlite3
from datetime import date

def create_tables():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    # Create table for student details
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                        ID INTEGER PRIMARY KEY,
                        Name TEXT NOT NULL,
                        ImagePath TEXT
                    )''')
    # Create table for attendance records
    cursor.execute('''CREATE TABLE IF NOT EXISTS Attendance (
                        ID INTEGER PRIMARY KEY,
                        StudentID INTEGER,
                        Date TEXT,
                        Time TEXT,
                        FOREIGN KEY(StudentID) REFERENCES Students(ID)
                    )''')
    conn.commit()
    conn.close()


def home(request):
    if request.method == 'POST' and 'takeAttendance' in request.POST:
        output_dir = os.path.join('daily_attendance', str(date.today()))  # Folder for today's attendance
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(0)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        image_count = 0
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

        cap.release()
        cv2.destroyAllWindows()

    profile_count = get_profile_count()
    return render(request, 'Home.html', {'profile_count': profile_count})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

def register(request):
    if request.method == 'GET':
        name = request.GET.get('name', '')

        if name:  
            save_profile_to_database(name)
            return render(request, "Take_image.html", {'Name': name})
        else:
            return render(request, "login.html")

def save_profile_to_database(name, image_path=None):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Students (Name) VALUES (?)", (name,))

    if image_path:
        cursor.execute("UPDATE Students SET ImagePath = ? WHERE Name = ?", (image_path, name))

    conn.commit()
    conn.close()

def take_images(request):
    if request.method == 'GET':
        output_dir = 'captured_images/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if 'take_image' in request.GET:
            cap = cv2.VideoCapture(0)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            image_count = 0
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

            cap.release()
            cv2.destroyAllWindows()

        if 'save_profile' in request.GET:
            cv2.destroyAllWindows() 
            cap.release()  
            return render(request, 'Take_image.html')

    return render(request, 'Take_image.html')

def get_profile_count():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Students")
    profile_count = cursor.fetchone()[0]
    conn.close()
    return profile_count
