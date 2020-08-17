import RPi.GPIO as GPIO
import MFRC522
import signal
from firebase import firebase
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
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
        key = [171,235,210,34,17]
        if (uid[0] == key[0] and uid[1] == key[1] and uid[2] == key[2] and uid[3] == key[3] and uid[4] == key[4]):
            result = 0
        return result
    def RFIDTask():
        MIFAREReader = RFID.Init()
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
                print ("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3],uid[4]))
                # This is the default key for authentication
                # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                key = [0xAB,0xEB,0xD2,0xFF,0x22,0xB0]
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)
                # Authenticate
                # status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 10, key, uid)
                status = RFID.Authen()
                # Check if authenticated
                if (status == MIFAREReader.MI_OK):
                    MIFAREReader.MFRC522_Read(10)
                    MIFAREReader.MFRC522_StopCrypto1()
                    print ("Authentication completed")
                else:
                    print ("Authentication error")
class FireBase_Com:
    def SendData():
        firebase = firebase.FirebaseApplication("https://test-firebase-7a605.firebaseio.com/",None)
        result = firebase.get('/addMeber', None)
        print(result)
if __name__ == "__main__":
    print("Starting...")
    # RFID.RFIDTask()
    FireBase_Com.SendData()