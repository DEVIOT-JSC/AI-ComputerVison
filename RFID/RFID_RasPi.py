import os
import threading
from threading import Thread
import RPi.GPIO as GPIO
import MFRC522
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from requests.packages import urllib3
import datetime
from time import sleep
# import signal
# from firebase import firebase
# Variable define 
hooman = ''
continue_reading = True
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
class Tools():
    def ReadIMGFile(path_to_file = ''):
        result = ''
        try:
            file = open(path_to_file,'r')
            line = file.readline()
            result = line
            os.remove(path_to_file)
            FaceIDReady = 1
        except:
            FaceIDReady = 0
        FaceIDReady = 0
        return FaceIDReady,result
    def GetKeyFromString(stringg = ''):
        uid_0 = int(stringg.split('-')[0])
        uid_1 = int(stringg.split('-')[1])
        uid_2 = int(stringg.split('-')[2])
        uid_3 = int(stringg.split('-')[3])
        uid_4 = int(stringg.split('-')[4])
        uid = [uid_0,uid_1,uid_2,uid_3,uid_4]
        return uid
    def GetStringFromList(uid_list = []):
        txt_uid = str(str(uid_list[0]) + '-' + str(uid_list[1]) + '-' + str(uid_list[2]) + '-' + str(uid_list[3]) + '-' + str(uid_list[4]))
        txt_uid = txt_uid.replace('[','').replace(']','')
        return txt_uid
class RFID:    
    def Init():
        # Hook the SIGINT
        GPIO.setmode(GPIO.BOARD)
        signal.signal(signal.SIGINT, end_read)
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()
        return MIFAREReader
    def Read():
        # MIFAREReader = RFID.Init()
        # GPIO.setmode(GPIO.BOARD)
        signal.signal(signal.SIGINT, end_read)
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()
        print("Mot con vit")
        print(continue_reading)
        while (continue_reading == True):
            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            # print(status)
            # If a card is found
            if (status == MIFAREReader.MI_OK):
                print("Card detected")
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if (status == MIFAREReader.MI_OK):

                # Print UID
                print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
            
                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # Check if authenticated
                if (status == MIFAREReader.MI_OK):
                    MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print ("Authentication error")
    def Write():
        while (continue_reading == True):
            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            # If a card is found
            if (status == MIFAREReader.MI_OK):
                print ("Card detected")
            
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if (status == MIFAREReader.MI_OK):

                # Print UID
                print ("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            
                # This is the default key for authentication
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
                print ("\n")

                # Check if authenticated
                if (status == MIFAREReader.MI_OK):

                    # Variable for the data to write
                    data = []

                    # Fill the data with 0xFF
                    for x in range(0,16):
                        data.append(0xFF)

                    print ("Sector 8 looked like this:")
                    # Read block 8
                    MIFAREReader.MFRC522_Read(8)
                    print ("\n")

                    print ("Sector 8 will now be filled with 0xFF:")
                    # Write the data
                    MIFAREReader.MFRC522_Write(8, data)
                    print ("\n")

                    print ("It now looks like this:")
                    # Check to see if it was written
                    MIFAREReader.MFRC522_Read(8)
                    print ("\n")

                    data = []
                    # Fill the data with 0x00
                    for x in range(0,16):
                        data.append(0x00)

                    print ("Now we fill it with 0x00:")
                    MIFAREReader.MFRC522_Write(8, data)
                    print ("\n")

                    print ("It is now empty:")
                    # Check to see if it was written
                    MIFAREReader.MFRC522_Read(8)
                    print ("\n")

                    # Stop
                    MIFAREReader.MFRC522_StopCrypto1()

                    # Make sure to stop reading for cards
                    continue_reading = False
                else:
                    print ("Authentication error")
    def Authen(uid = []):
        i = 0
        list_UserID = []
        list_UserInfo = []
        str_uid = str(uid)
        list_UserID,list_UserInfo = FireBase_Com.GetAuthenData()
        for ls in list_UserInfo:
            cmp_stt = str(ls).find(str_uid)
            if (cmp_stt != -1):
                result = 1
            else:
                result = 0
                i = i+1
        # if (uid[0] == key[0] and uid[1] == key[1] and uid[2] == key[2] and uid[3] == key[3] and uid[4] == key[4]):
        #     result = 0
        UsrID = list_UserID[i]
        return result,UsrID
    def AuthenFace(FaceID = []):
        i = 0
        list_UserID = []
        list_UserInfo = []
        list_UserID,list_UserInfo = FireBase_Com.GetAuthenData()
        for ls in list_UserInfo:
            cmp_stt = str(ls).find(FaceID)
            if (cmp_stt != -1):
                result = 1
            else:
                result = 0
                i = i+1
        # if (uid[0] == key[0] and uid[1] == key[1] and uid[2] == key[2] and uid[3] == key[3] and uid[4] == key[4]):
        #     result = 0
        UsrID = list_UserID[i]
        return result,UsrID
    def RFIDTask():
        MIFAREReader = RFID.Init()
        while (continue_reading == True):
            AddSig,NewUsrID,appRq = FireBase_Com.AddNew()
            if (appRq == '0' or appRq == '1'):
                print("Looking for card...")
                # Scan for cards    
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                # If a card is found
                if (status == MIFAREReader.MI_OK):
                    print ("Card detected")
                
                # Get the UID of the card
                (status,uid) = MIFAREReader.MFRC522_Anticoll()

                # If we have the UID, continue
                if (status == MIFAREReader.MI_OK):
                    # Print UID
                    print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
                    # This is the default key for authentication
                    # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                    key = [0xAB,0xEB,0xD2,0xFF,0x22,0xB0]
                    # Select the scanned tag
                    MIFAREReader.MFRC522_SelectTag(uid)
                    # Authenticate
                    # status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 10, key, uid)
                    if (appRq == '0'): #RFID Card
                        txt_uid = Tools.GetStringFromList(uid)
                        AutStt,UsrID = RFID.Authen(txt_uid)
                        if (AutStt == 1):
                            FireBase_Com.SendData(txt_uid,UsrID)
                    elif (appRq == '1'): #Add Card
                        print("Add new id card")
                        FireBase_Com.UpdateCardInfo(NewUsrID,uid)
                    # Check if authenticated
                    # if (status == MIFAREReader.MI_OK):
                    #     MIFAREReader.MFRC522_Read(10)
                    #     MIFAREReader.MFRC522_StopCrypto1()
                    #     print ("Authentication completed")
                    # else:
                    #     print ("Authentication error")
            elif (appRq == '2'):
                print("Add new Face ID")
                FireBase_Com.UpdateFaceInfo(NewUsrID,FaceID)
class FaceDetection:
    def GetFace():
        print("Looking for new face...")
        # Sig,FaceID = Tools.ReadIMGFile('path')
        while(1):
            result,UsrID = RFID.AuthenFace(FaceID)
            if(result == 1):
                FireBase_Com(result,UsrID)
class FireBase_Com:
    def Init():
        # cred = credentials.Certificate("test-firebase-7a605-firebase-adminsdk-ge9h3-e2a3245f8b.json")
        # firebase_admin.initialize_app(cred,{'databaseURL':'https://test-firebase-7a605.firebaseio.com'})
        cred = credentials.Certificate("deviot-may-cham-cong-firebase-adminsdk-4j9vd-c20046ba51.json")
        firebase_admin.initialize_app(cred,{'databaseURL':'https://deviot-may-cham-cong.firebaseio.com'})
    def AddNew():
        tmp_vr = []
        FireBase_Com.Init()
        addMember = db.reference('addMember')
        addTab = addMember.get()
        print(addTab)
        # json_addTab = json.dumps(addTab)
        for key, value in addTab.items():
            tmp_vr.append(value)
        NewUsrID = tmp_vr[0]
        appRq = tmp_vr[1]
        return str(addTab),NewUsrID,appRq
    def SendData(txt_uid='',UsrID=''):
        # Init connection
        # cred = credentials.Certificate("test-firebase-7a605-firebase-adminsdk-ge9h3-e2a3245f8b.json")
        # firebase_admin.initialize_app(cred,{'databaseURL':'https://test-firebase-7a605.firebaseio.com'})
        FireBase_Com.Init()
        today = str(datetime.datetime.today()).split(" ")[0]
        # Send data
        diemdanh = db.reference(str('diemdanh/'+today))
        # diemdanh = db.reference(str('diemdanh/13-08-2020'))
        rq = diemdanh.child(UsrID)
        now = datetime.datetime.now()
        timeEnter = '0'
        timeExit = '0'
        hour = int(str(now).split(' ')[1].split(':')[0])
        this_time = str(now).split(' ')[1].split('.')[0]
        if (hour > 8 and hour < 10):
            timeEnter = this_time
            result = rq.update({'timeEnter':timeEnter})
        elif (hour > 16 and hour < 18):
            timeExit = this_time
            result = rq.update({'timeExit':timeExit})
        # result = rq.update({'timeEnter':timeEnter,
        #                     'timeExit':timeExit})
        # print(result)
    def GetAuthenData():
        FireBase_Com.Init()
        list_UserID = []
        list_UserInfo = []
        #Get data
        # dd_child = '112-52-29-164-253'
        # diemdanh = db.reference(str('employees/'+dd_child))
        employees = db.reference('employees')
        dayTab = employees.get()
        # print(str(dayTab).replace("'",'"'))
        json_dayTab = json.dumps(dayTab)
        for key, value in dayTab.items():
            list_UserID.append(key)
            list_UserInfo.append(value)
        # json_str = json.load(dayTab)
        # json_str = json.load(str(str(dayTab).replace("'",'"')))
        # print(dayTab)
        # print(type(dayTab))
        # Get list Main ID
        return list_UserID,list_UserInfo
    def UpdateCardInfo(UsrID = '', CardID = ''):
        FireBase_Com.Init()
        employees = db.reference(str('employees/'+UsrID))
        result = employees.update({'id':UsrID})
    def UpdateFaceInfo(UsrID = '', FaceID = ''):
        FireBase_Com.Init()
        employees = db.reference(str('employees/'+UsrID))
        result = employees.update({'FaceID':FaceID})
def MainThread():
    RFID.RFIDTask()
    # print('Main')
def FaceThread():
    # FaceDetection.GetFace()
    sleep(10)
    print('Face')
if __name__ == "__main__":
    print("Starting...")
    while(1):
        MainTh = threading.Thread(target = MainThread)
        FaceTh = threading.Thread(target = FaceThread)
        MainTh.start()
        FaceTh.start()
