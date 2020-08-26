import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime



# path = 'data/'
# images = []
# myList = os.listdir(path)
# print(myList)
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
# classNames=['anh', 'huong', 'tuan', 'tung']
# tentxt=['anh.txt', 'huong.txt', 'tuan.txt', 'tung.txt']
# #
# def findEncodings(images,tentxt):
#     for (img, tentxt2) in zip(images,tentxt):
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         np.savetxt(tentxt2,encode)
# encodeListKnown = findEncodings(images,tentxt)

##########
path = 'data'
new_img='tam.jpg'
new_txt='tam.txt'
path_img=os.path.sep.join([path, new_img])
Img = cv2.imread(path_img,1)
img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
encode = face_recognition.face_encodings(img)[0]
np.savetxt(new_txt, encode)

##########
# classNames=['anh', 'huong', 'tuan', 'tung','trung','giang','hai','hung','ha','huy','thon','nam','giangdc','hoang','tam','anh_tuan']
# tentxt=['anh.txt', 'huong.txt', 'tuan.txt', 'tung.txt','trung.txt','giang.txt','hai.txt','hung.txt','ha.txt','huy.txt','thon.txt','nam.txt','giangdc.txt','hoang.txt','tam.txt','anh_tuan.txt']
# encodeListKnown=[]
# for i2 in tentxt:
#     i3=np.loadtxt(i2)
#     encodeListKnown.append(i3)
# encodeListKnown=np.array(encodeListKnown)
#
#
# img = cv2.imread('anh_tuan.jpg',1)
# imgS = cv2.resize(img, (720,960))
# imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
# detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# rects = detector.detectMultiScale(imgS, scaleFactor=1.1,
#                                   minNeighbors=5, minSize=(30, 30),
#                                   flags=cv2.CASCADE_SCALE_IMAGE)
# boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
# boxes=np.array(boxes)
# print(boxes)
#
# a = int(boxes[:, 0])
# b = int(boxes[:, 1])
# c = int(boxes[:, 2])
# d = int(boxes[:, 3])
#
# boxes1 = [(a, b, c, d)]
#
# encodesCurFrame = face_recognition.face_encodings(imgS, boxes1)
#
#
# matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame)
# faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
# matchIndex = np.argmin(faceDis)
#
# if matches[matchIndex]:
#     name = classNames[matchIndex].upper()
#     print(name)
#     y1= boxes[:,0]
#     x2 = boxes[:,1]
#     y2= boxes[:,2]
#     x1 = boxes[:,3]
#     cv2.rectangle(imgS, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     cv2.rectangle(imgS, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#     cv2.putText(imgS, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
#
# cv2.namedWindow('iamge',cv2.WINDOW_NORMAL)
# cv2.imshow('iamge', imgS)
# cv2.waitKey(0)