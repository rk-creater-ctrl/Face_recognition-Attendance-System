import cv2
import os
from tkinter import Tk, simpledialog, messagebox


Tk().withdraw()

name = simpledialog.askstring("Student Name", "Enter student name:")
if not name:
    messagebox.showerror("Error", "Name cannot be empty")
    exit()

base_path = "dataset"
person_path = os.path.join(base_path, name)
os.makedirs(person_path, exist_ok=True)

cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(person_path, f"{count}.jpg"), face)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("Capturing Faces", frame)

    if cv2.waitKey(1) == 27 or count >= 50:
        break

cam.release()
cv2.destroyAllWindows()
messagebox.showinfo("Done", f"Images captured for {name}")
