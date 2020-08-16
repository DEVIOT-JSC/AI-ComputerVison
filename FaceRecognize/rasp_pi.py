from imutils.video import VideoStream
import face_recognition
import time
import cv2
import numpy as np
from datetime import datetime
import os
import matplotlib.pyplot as plt
from imutils.video import FPS
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
# path = 'data'
# new_img='tam.jpg'
# new_txt='tam.txt'
# path_img=os.path.sep.join([path, new_img])
# Img = cv2.imread(path_img,1)
# img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
# encode = face_recognition.face_encodings(img)[0]
# np.savetxt(new_txt, encode)

nameList = []
# vs = VideoStream(src=1).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
tt1 = True

# camera = PiCamera()
# camera.resolution = (300, 300)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(300, 300))
# nameList = []
# # vs = VideoStream(src=1).start()
# # vs = VideoStream(usePiCamera=True).start()
# time.sleep(2.0)
# tt1 = True

classNames = ['anh', 'huong', 'tuan', 'tung', 'trung', 'giang', 'hai', 'hung', 'ha', 'huy', 'thon', 'nam',
              'giangdc', 'hoang', 'tam','anh_tuan']
tentxt = ['/home/pi/face_recog/anh.txt', '/home/pi/face_recog/huong.txt', '/home/pi/face_recog/tuan.txt', '/home/pi/face_recog/tung.txt',
          '/home/pi/face_recog/trung.txt', '/home/pi/face_recog/giang.txt', '/home/pi/face_recog/hai.txt', '/home/pi/face_recog/hung.txt',
          '/home/pi/face_recog/ha.txt',
          '/home/pi/face_recog/huy.txt', '/home/pi/face_recog/thon.txt', '/home/pi/face_recog/nam.txt', '/home/pi/face_recog/giangdc.txt',
          '/home/pi/face_recog/hoang.txt', '/home/pi/face_recog/tam.txt','/home/pi/face_recog/anh_tuan.txt']
encodeListKnown = []
for i2 in tentxt:
    i3 = np.loadtxt(i2)
    encodeListKnown.append(i3)
encodeListKnown = np.array(encodeListKnown)


with open('/home/pi/face_recog/lich_cham_cong.csv', 'r+') as f:
    date = datetime.today().date()
    now = datetime.now()
    date = date.strftime('%d/%m/%Y')
    dtString = now.strftime('%H:%M:%S')
    f.writelines(f'\n{date},{dtString}')
fps = FPS().start()

while tt1 == True:

    tt = True
    while tt == True:
    # for frame1 in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):

        frame = vs.read()
        h = frame.shape[0]
        w = frame.shape[1]
        # print(h)
        # print(w)
        # frame = cv2.resize(frame, (500, ))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
        rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = np.array(boxes)
        # print(boxes)
        if (len(boxes) != 1):
            cv2.putText(frame, 'khong co ai', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0,0 , 255), 2)
            cv2.imshow('frame',frame)
            key = cv2.waitKey(1)& 0xFF
            fps.update()
            # rawCapture.truncate(0)
            continue
        a = int(boxes[:, 0])
        b = int(boxes[:, 1])
        c = int(boxes[:, 2])
        d = int(boxes[:, 3])
        boxes1 = [(a, b, c, d)]
        # print(boxes1)


        if ((10 > a or a > 130) or (170 > b or b > 320) or (70 > c or 230 < c) or (70 > d or 250 < d)):
            cv2.putText(frame, 'chua vao dung vi tri', (25, 150), cv2.FONT_HERSHEY_SIMPLEX,
                       0.75, (255, 0, 0), 2)
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
            time.sleep(0.1)
            # cv2.destroyAllWindows()
            continue
        else:
            # frame2=frame
            print('da dung vi tri')
            cv2.putText(frame, 'du nguyen vi tri', (20, 150), cv2.FONT_HERSHEY_SIMPLEX,
                       0.75, (0, 255, 0), 2)
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
            time.sleep(1)


        # frame = frame1.array
        frame = vs .read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
        rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = np.array(boxes)
        # print(boxes)
        if (len(boxes) != 1):
            continue
        a = int(boxes[:, 0])
        b = int(boxes[:, 1])
        c = int(boxes[:, 2])
        d = int(boxes[:, 3])
        boxes1 = [(a, b, c, d)]
        print('buoc tipe theo')
        # rawCapture.truncate(0)
        cv2.destroyAllWindows()
        break

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # do a bit of cleanup
    # stream.release()
    cv2.destroyAllWindows()

    encodesCurFrame = face_recognition.face_encodings(frame, boxes1)
    matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame)
    faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
    matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
        with open('/home/pi/face_recog/lich_cham_cong.csv', 'r+') as f:
            myDataList = f.readlines()

            # for line in myDataList:
            #     entry = line.split(',')
            #     nameList.append(entry[0])
            if name not in nameList:
                nameList.append(name)
                now = datetime.now()
                date = datetime.today().date()
                date=date.strftime('%d/%m/%Y')
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{date},{dtString}')
            else:
                # frame3=frame
                plt.clf()
                cv2.putText(frame, name, (20, 150), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
                cv2.putText(frame,'khong the', (150, 150), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
                cv2.putText(frame, 'cham cong 2 lan', (50, 200), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
                plt.imshow(frame)
                plt.ion()
                plt.show()
                plt.pause(0.5)
                plt.clf()
                # cv2.imshow('khong the', frame)
                # cv2.waitKey(1)
                # time.sleep()


                continue
        y1 = boxes[:, 0]
        x2 = boxes[:, 1]
        y2 = boxes[:, 2]
        x1 = boxes[:, 3]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 2)
        # print(name)
        # # plt.clf()
        cv2.putText(frame, 'da cham cong', (0, 50), cv2.FONT_HERSHEY_COMPLEX,0.75, (0, 255, 0), 2)
        # cv2.imshow('da cham cong',frame)
        # cv2.waitKey(1)
        # time.sleep(3)
        plt.imshow(frame)
        plt.ion()
        plt.show()
        plt.pause(0.5)
        plt.clf()
    else:
        plt.clf()
        cv2.putText(frame, 'chua the nhan dien ', (int(h/2-200), int(w/2-40)), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(frame, 'xin hay chup lai ', (int(h/2-200), int(w/2+10)), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
        plt.imshow(frame)
        plt.ion()
        plt.show()
        plt.pause(0.5)
        plt.clf()
        continue




# from imutils.video import VideoStream
# import face_recognition
# import time
# import cv2
# import numpy as np
# from datetime import datetime
# import os
# import matplotlib.pyplot as plt


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
# path = 'data'
# new_img='tam.jpg'
# new_txt='tam.txt'
# path_img=os.path.sep.join([path, new_img])
# Img = cv2.imread(path_img,1)
# img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
# encode = face_recognition.face_encodings(img)[0]
# np.savetxt(new_txt, encode)



# camera = PiCamera()
# camera.resolution = (300, 300)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(300, 300))
# nameList = []
# # vs = VideoStream(src=1).start()
# # vs = VideoStream(usePiCamera=True).start()
# time.sleep(2.0)
# tt1 = True
#
# classNames = ['anh', 'huong', 'tuan', 'tung', 'trung', 'giang', 'hai', 'hung', 'ha', 'huy', 'thon', 'nam',
#               'giangdc', 'hoang', 'tam','anh_tuan']
# tentxt = ['/home/pi/face_recog/anh.txt', '/home/pi/face_recog/huong.txt', '/home/pi/face_recog/tuan.txt', '/home/pi/face_recog/tung.txt',
#           '/home/pi/face_recog/trung.txt', '/home/pi/face_recog/giang.txt', '/home/pi/face_recog/hai.txt', '/home/pi/face_recog/hung.txt',
#           '/home/pi/face_recog/ha.txt',
#           '/home/pi/face_recog/huy.txt', '/home/pi/face_recog/thon.txt', '/home/pi/face_recog/nam.txt', '/home/pi/face_recog/giangdc.txt',
#           '/home/pi/face_recog/hoang.txt', '/home/pi/face_recog/tam.txt','/home/pi/face_recog/anh_tuan.txt']
# encodeListKnown = []
# for i2 in tentxt:
#     i3 = np.loadtxt(i2)
#     encodeListKnown.append(i3)
# encodeListKnown = np.array(encodeListKnown)
#
#
# with open('/home/pi/face_recog/lich_cham_cong.csv', 'r+') as f:
#     date = datetime.today().date()
#     now = datetime.now()
#     date = date.strftime('%d/%m/%Y')
#     dtString = now.strftime('%H:%M:%S')
#     f.writelines(f'\n{date},{dtString}')
#
#
# while tt1 == True:
#     tt = True
#     for frame1 in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
#
#         frame = frame1.array
#         h=frame.shape[0]
#         w=frame.shape[1]
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
#         rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                           minNeighbors=5, minSize=(30, 30),
#                                           flags=cv2.CASCADE_SCALE_IMAGE)
#         boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#         boxes = np.array(boxes)
#         if (len(boxes) != 1):
#             cv2.putText(frame, 'khong co ai', (150, 150), cv2.FONT_HERSHEY_SIMPLEX,
#                        1, (0,0 , 255), 2)
#             cv2.imshow('khong co ai',frame)
#             key = cv2.waitKey(1)& 0xFF
#             rawCapture.truncate(0)
#             continue
#         a = int(boxes[:, 0])
#         b = int(boxes[:, 1])
#         c = int(boxes[:, 2])
#         d = int(boxes[:, 3])
#         boxes1 = [(a, b, c, d)]
#         # print(boxes1)
#
#
#         if ((10 > a or a > 150) or (200 > b or b > 600) or (180 > c or 600 < c) or (10 > d or 300 < d)):
#             cv2.putText(frame, 'chua vao dung vi tri', (25, 250), cv2.FONT_HERSHEY_SIMPLEX,
#                        0.75, (255, 0, 0), 2)
#             cv2.imshow('chua vao vi tri',frame)
#             cv2.waitKey(1)
#             continue
#         else:
#             frame2=frame
#             cv2.putText(frame2, 'du nguyen vi tri', (250, 250), cv2.FONT_HERSHEY_SIMPLEX,
#                        0.75, (0, 255, 0), 2)
#             plt.imshow(frame2)
#             plt.ion()
#             plt.show()
#             # plt.pause(0.5)
#             plt.clf()
#
#
#         frame = frame1.array
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
#         rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
#                                           minNeighbors=5, minSize=(30, 30),
#                                           flags=cv2.CASCADE_SCALE_IMAGE)
#         boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
#         boxes = np.array(boxes)
#         print(boxes)
#         if (len(boxes) != 1):
#             continue
#         a = int(boxes[:, 0])
#         b = int(boxes[:, 1])
#         c = int(boxes[:, 2])
#         d = int(boxes[:, 3])
#         boxes1 = [(a, b, c, d)]
#         rawCapture.truncate(0)
#         cv2.destroyAllWindows()
#         break
#
#     encodesCurFrame = face_recognition.face_encodings(frame, boxes1)
#     matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame)
#     faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
#     matchIndex = np.argmin(faceDis)
#
#     if matches[matchIndex]:
#         name = classNames[matchIndex].upper()
#         with open('/home/pi/face_recog/lich_cham_cong.csv', 'r+') as f:
#             myDataList = f.readlines()
#
#             # for line in myDataList:
#             #     entry = line.split(',')
#             #     nameList.append(entry[0])
#             if name not in nameList:
#                 nameList.append(name)
#                 now = datetime.now()
#                 date = datetime.today().date()
#                 date=date.strftime('%d/%m/%Y')
#                 dtString = now.strftime('%H:%M:%S')
#                 f.writelines(f'\n{name},{date},{dtString}')
#             else:
#                 # frame3=frame
#                 plt.clf()
#                 cv2.putText(frame, name, (50, 150), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
#                 cv2.putText(frame,'khong the', (150, 150), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
#                 cv2.putText(frame, 'cham cong 2 lan', (50, 250), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
#                 plt.imshow(frame)
#                 plt.ion()
#                 plt.show()
#                 plt.pause(1)
#                 plt.clf()
#
#                 continue
#         y1 = boxes[:, 0]
#         x2 = boxes[:, 1]
#         y2 = boxes[:, 2]
#         x1 = boxes[:, 3]
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#         cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 255, 255), 2)
#         print(name)
#         plt.clf()
#         cv2.putText(frame, 'da cham cong', (0, 50), cv2.FONT_HERSHEY_COMPLEX,0.75, (0, 255, 0), 2)
#         plt.imshow(frame)
#         plt.ion()
#         plt.show()
#         plt.pause(1)
#         plt.clf()
#     else:
#         plt.clf()
#         cv2.putText(frame, 'chua the nhan dien ', (int(h/2-200), int(w/2-40)), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
#         cv2.putText(frame, 'xin hay chup lai ', (int(h/2-200), int(w/2+10)), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
#         plt.imshow(frame)
#         plt.ion()
#         plt.show()
#         plt.pause(1)
#         plt.clf()
#         continue

