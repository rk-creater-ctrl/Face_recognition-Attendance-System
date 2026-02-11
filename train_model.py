import cv2
import numpy as np
import os
from tkinter import messagebox, Tk


Tk().withdraw()

dataset_path = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}
label_id = 0

for person in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person)
    if not os.path.isdir(person_path):
        continue

    label_map[label_id] = person

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        faces.append(img)
        labels.append(label_id)

    label_id += 1

recognizer.train(faces, np.array(labels))
recognizer.save("trainer.yml")

with open("labels.txt", "w") as f:
    for k, v in label_map.items():
        f.write(f"{k},{v}\n")

messagebox.showinfo("Success", "Model trained successfully!")
