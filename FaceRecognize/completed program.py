from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import time
import cv2
import numpy as np
from datetime import datetime
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library



def button_callback(channel):
    with open('lich_cham_cong.csv', 'r+') as f:
        myDataList = f.readlines()




    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
    message = input("Press enter to quit\n\n") # Run until someone presses enter
    GPIO.cleanup() # Clean up











nameList = []
vs = VideoStream(src=1).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
tt1 = True

classNames = ['anh', 'huong', 'tuan', 'tung', 'trung', 'giang', 'hai', 'hung', 'ha', 'huy', 'thon', 'nam',
              'giangdc', 'hoang', 'tam']
tentxt = ['anh.txt', 'huong.txt', 'tuan.txt', 'tung.txt', 'trung.txt', 'giang.txt', 'hai.txt', 'hung.txt', 'ha.txt',
          'huy.txt', 'thon.txt', 'nam.txt', 'giangdc.txt', 'hoang.txt', 'tam.txt']
encodeListKnown = []
for i2 in tentxt:
    i3 = np.loadtxt(i2)
    encodeListKnown.append(i3)
encodeListKnown = np.array(encodeListKnown)


with open('lich_cham_cong.csv', 'r+') as f:
    date = datetime.today().date()
    now = datetime.now()
    date = date.strftime('%d/%m/%Y')
    dtString = now.strftime('%H:%M:%S')
    f.writelines(f'\n{date},{dtString}')


while tt1 == True:
    tt = True
    while tt == True:
        frame = vs.read()
        h=frame.shape[0]
        w=frame.shape[1]
        # frameS = cv2.resize(frame, (720, 960))
        imgS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = np.array(boxes)
        if (len(boxes) != 1):
            cv2.putText(frame, 'khong co ai', (150, 150), cv2.FONT_HERSHEY_SIMPLEX,
                       2, (0,0 , 255), 2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            continue
        a = int(boxes[:, 0])
        b = int(boxes[:, 1])
        c = int(boxes[:, 2])
        d = int(boxes[:, 3])
        boxes1 = [(a, b, c, d)]


        if ((10 > a or a > 150) or (310 > b or b > 600) or (250 > c or 600 < c) or (60 > d or 300 < d)):
            cv2.putText(frame, 'chua vao dung vi tri', (25, 250), cv2.FONT_HERSHEY_SIMPLEX,
                       1.5, (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)
            continue
        else:
            cv2.putText(frame, 'du nguyen vi tri', (250, 250), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0, 255, 0), 2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
        time.sleep(1)
        frame = vs.read()

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = np.array(boxes)
        if (len(boxes) != 1):
            continue
        a = int(boxes[:, 0])
        b = int(boxes[:, 1])
        c = int(boxes[:, 2])
        d = int(boxes[:, 3])
        boxes1 = [(a, b, c, d)]
        cv2.destroyAllWindows()
        tt = False

    encodesCurFrame = face_recognition.face_encodings(frame, boxes1)
    matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame)
    faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
    matchIndex = np.argmin(faceDis)

    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
        with open('lich_cham_cong.csv', 'r+') as f:
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
                cv2.putText(frame, name, (50, 250), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                cv2.putText(frame,'khong the', (350, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, 'cham cong 2 lan', (50, 300), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('iamge', frame)
                cv2.waitKey(3)
                time.sleep(3)
                cv2.destroyAllWindows()
                continue
        y1 = boxes[:, 0]
        x2 = boxes[:, 1]
        y2 = boxes[:, 2]
        x1 = boxes[:, 3]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, 'da cham cong', (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 2)
        cv2.imshow('iamge', frame)
        cv2.waitKey(3)
        time.sleep(3)
        cv2.destroyAllWindows()


    else:
        cv2.putText(frame, 'chua the nhan dien ', (int(h/2-200), int(w/2-40)), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)
        cv2.putText(frame, 'xin hay chup lai ', (int(h/2-200), int(w/2+10)), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)
        cv2.imshow('iamge', frame)
        cv2.waitKey(3)
        time.sleep(5)
        cv2.destroyAllWindows()
        continue



