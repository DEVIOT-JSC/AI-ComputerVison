
from imutils.video import VideoStream
import time
import cv2
import numpy as np
from datetime import datetime
import os
# import matplotlib.pyplot as plt
from imutils.video import FPS
import urllib.request
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from requests.packages import urllib3
import json
cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
def AddNew():
    tmp_vr = []
    # FireBase_Com.Init()
    addMember = db.reference('addMember')
    addTab = addMember.get()
    # print(addTab)
    # json_addTab = json.dumps(addTab)
    # for key, value in addTab.items():
    #     tmp_vr.append(value)
    dbNewUsrID = db.reference('addMember/NewUsrID')
    dbappRq = db.reference('addMember/appRequest')
    NewUsrID = dbNewUsrID.get()
    appRq = dbappRq.get()
    print("NewUsrID",NewUsrID)
    print("appRequest",appRq)
    return str(addTab),NewUsrID,appRq
def ReverseDay(day = ''):
    # 2020-08-27
    ls_par = day.split('-')
    output = ''
    for i in range (0, len(ls_par)):
        if (output != ''):
            output = output + '-' + ls_par[len(ls_par)-1-i]
        else:
            output = output + ls_par[len(ls_par)-1-i]
    print(output)
    return output
def SendData(UsrID=''):
    today = ReverseDay(str(datetime.datetime.today()).split(" ")[0])
    # Send data
    diemdanh = db.reference(str('diemdanh/'+today))
    print("str('diemdanh/'+today)",str('diemdanh/'+today))
    # diemdanh = db.reference(str('diemdanh/13-08-2020'))
    rq = diemdanh.child(UsrID)
    now = datetime.datetime.now()
    timeEnter = '0'
    timeExit = '0'
    hour = int(str(now).split(' ')[1].split(':')[0])
    this_time = str(now).split(' ')[1].split('.')[0]
    print(this_time)
    # print('hour = ',hour)
    print('this time',this_time)
    if (hour > 8 and hour < 10):
        timeEnter = this_time
        result = rq.update({'timeEnter':timeEnter})
    elif (hour > 16 and hour < 18):
        timeExit = this_time
        result = rq.update({'timeExit':timeExit})
def Authen(uid = []):
    i = 0
    list_UserID = []
    list_UserRFID = []
    str_uid = str(uid)
    list_UserID,list_UserFaceID = GetAuthenData()
    print(list_UserFaceID)
    try:
        for ls in list_UserFaceID:
            cmp_stt = str(ls).find(str_uid)
            if (cmp_stt != -1):
                result = 1
                break
            else:
                result = 0
                i = i+1
        if (result == 1):
            print("ACCESS GRANTED!!!")
        else:
            print("ACESS DENIED")
        print("\ni = ",i)
        print(list_UserID)
        UsrID = list_UserID[i]
    except:
        print("       ")
        UsrID = ''
    i= 0
    return result,UsrID
def GetAuthenData():
    # FireBase_Com.Init()
    list_UserID = []
    list_UserFaceID = []
    list_UserInfo = []
    #Get data
    employees = db.reference('employees')
    dayTab = employees.get()
    json_dayTab = json.dumps(dayTab)
    for key, value in dayTab.items():
        list_UserID.append(key)
        list_UserInfo.append(value)
    for id in list_UserID:
        db_faceid = db.reference(str('employees/' + str(id) + '/FaceID'))
        faceid_ = db_faceid.get()
        list_UserFaceID.append(faceid_)
    return list_UserID,list_UserFaceID
def UpdateFaceInfo(UsrID = '', FaceID = ''):
    # FireBase_Com.Init()
    employees = db.reference(str('employees/'+UsrID))
    result = employees.update({'FaceID':FaceID})
def PushDataToFirebase(FaceID = ''):
    # Connect to firebase
    # cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
    # firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
    addTab,NewUsrID,appRq = AddNew()
    if (appRq == 2):
        UpdateFaceInfo(NewUsrID,FaceID)
    else:
        result,UsrID = Authen(FaceID)
        if (result == 1):
            SendData(UsrID)
            print("Access Granted")
        else:
            print("Access Denied")
    db_reset_appRq = db.reference('addMember')
    rs = db_reset_appRq.update({'appRequest':0})
def GetImageInfo():
    dbImgID = db.reference('addMember/idAnh')
    idAnh = dbImgID.get()
    dbImgUrl = db.reference('addMember/linkAnh')
    url = dbImgUrl.get()
    return idAnh,url



# def remove_comma(name_file):
#     with open(name_file, 'r') as f:
#         content = f.readline()
#     content=list(content.split(','))
#     content.remove('')
#     return content

with open('danh_sach_ten.txt', 'r') as f:
    classNames = f.readline()
classNames=list(classNames.split(','))
classNames.remove('')

with open('danh_sach_text.txt', 'r') as f:
    tentxt = f.readline()
tentxt=list(tentxt.split(','))
tentxt.remove('')

print(type(tentxt))

with open('danh_sach_text.txt', 'r') as f:
    tentxt = f.readline()
tentxt=list(tentxt.split(','))
tentxt.remove('')

print(type(tentxt))

with open('danh_sach_id.txt', 'r') as f:
    DS_ID = f.readline()
DS_ID=list(DS_ID.split(','))
DS_ID.remove('')


_,_,request=AddNew()

if request==1:
    idAnh,url=GetImageInfo()
    ten = idAnh.split('_')[0]
    new_img=ten+'.jpg'
    new_txt=ten+'.txt'
    classNames.append(ten)
    len_classNames=len(classNames)
    with open('/home/pi/face_recog/danh_sach_ten.txt', 'a') as f:
        ten1=ten+','
        f.writelines(f'{ten1}')

    DS_ID.append(idAnh)
    len_DS_ID=len(DS_ID)
    with open('danh_sach_id.txt', 'a') as f:
        idAnh1=idAnh+','
        f.writelines(f'{idAnh1}')
    newtentxt='/home/pi/face_recog/'+new_txt
    tentxt.append(newtentxt)
    len_tentxt=len(tentxt)

    with open('/home/pi/face_recog/danh_sach_text.txt', 'a') as f:
        newtentxt1=newtentxt+','
        f.writelines(f'{newtentxt1}')


    file_path='/home/pi/face_recog/data'
    full_path=os.path.sep.join([file_path, new_img])
    urllib.request.urlretrieve(url,full_path)
    path = '/home/pi/face_recog/data'
    path_img = os.path.sep.join([path, new_img])
    Img = cv2.imread(path_img, 1)
    img = cv2.cvtColor(Img, cv2.COLOR_BGR2RGB)
    detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
    rects = detector.detectMultiScale(img, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    boxes = np.array(boxes)
    a = int(boxes[:, 0])
    b = int(boxes[:, 1])
    c = int(boxes[:, 2])
    d = int(boxes[:, 3])
    boxes1 = [(a, b, c, d)]
    encode = face_recognition.face_encodings(img,boxes1)
    np.savetxt(new_txt, encode)
    print('da save')

nameList = []
# vs = VideoStream(src=1).start()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
encodeListKnown = []
for i2 in tentxt:
    i3 = np.loadtxt(i2)
    encodeListKnown.append(i3)
encodeListKnown = np.array(encodeListKnown)


while True:
    name = ''
    while True:
        frame = vs.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
        rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = np.array(boxes)

        if (len(boxes) != 1 or len_classNames==0 or len_DS_ID==0 or len_tentxt==0):
            cv2.putText(frame, 'khong co ai', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0,0 , 255), 2)
            cv2.imshow('frame',frame)
            key = cv2.waitKey(1)& 0xFF
            continue
        else:
            a = int(boxes[:, 0])
            b = int(boxes[:, 1])
            c = int(boxes[:, 2])
            d = int(boxes[:, 3])
            face=frame[b:d,a:c]
            face=np.array(face)
            # print(type(face))
            (fh,fw)=face.shape[:2]
            # print(fw)
            # if fw < 80:
            #     continue

            # start = time.time()

            cv2.putText(frame, 'STOP', (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                       1, (0,0 , 255), 2)
            cv2.imshow('frame',frame)
            key = cv2.waitKey(1)& 0xFF
            time.sleep(1)
            frame=vs.read()
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
            rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
            boxes = np.array(boxes)

            if (len(boxes) == 1):
                a = int(boxes[:, 0])
                b = int(boxes[:, 1])
                c = int(boxes[:, 2])
                d = int(boxes[:, 3])
                boxes1 = [(a, b, c, d)]
                break
            else:
                continue

    encodesCurFrame = face_recognition.face_encodings(frame, boxes1)
    matches = face_recognition.compare_faces(encodeListKnown, encodesCurFrame, tolerance=0.5)
    faceDis = face_recognition.face_distance(encodeListKnown, encodesCurFrame)
    matchIndex = np.argmin(faceDis)
    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
        ID=DS_ID[matchIndex]
        print(ID)
        PushDataToFirebase(ID)
        if name=='':
            continue
        with open('/home/pi/face_recog/lich_cham_cong.txt', 'a') as f:
            # myDataList = f.readlines()
            if name not in nameList:
                nameList.append(name)
                f.writelines(f'{name}\n')

    while(True):
        frame = vs.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detector = cv2.CascadeClassifier('/home/pi/face_recog/haarcascade_frontalface_default.xml')
        rects = detector.detectMultiScale(rgb, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = np.array(boxes)
        # end = time.time()
        # tg = end - start
        # print(tg)

        if (len(boxes) == 1):
            a = int(boxes[:, 0])
            b = int(boxes[:, 1])
            c = int(boxes[:, 2])
            d = int(boxes[:, 3])
            cv2.putText(frame, name, (d + 6, c - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 0), 2)
            cv2.rectangle(frame, (d, a), (b, c), (0, 255, 0), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        else:
            break

