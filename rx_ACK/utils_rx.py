from __future__ import print_function
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import struct

radio2 = NRF24(GPIO, spidev.SpiDev())

def init_radio(payload, datarate, palevel, pipe, autrotrack, channel, retries, begin):
    print("[*] Starting Radio Interface...")
    radio2.begin(begin[0], begin[1])

    radio2.setRetries(retries[0],retries[1])

    radio2.setPayloadSize(payload)
    radio2.setChannel(channel)
    radio2.setDataRate(datarate)
    radio2.setPALevel(palevel)

    radio2.setAutoAck(autrotrack)
    radio2.enableDynamicPayloads()
    radio2.enableAckPayload()

    radio2.openWritingPipe(pipe[0])
    radio2.openReadingPipe(1, pipe[1])

    radio2.startListening()
    radio2.stopListening()
    radio2.printDetails()

    radio2.startListening()

def receive_data():
    print("\n\n\n\n*****Quick mode*****\n\nWaiting for data...")

    c = 0

    file = open("text.txt", "w")
    pipe = [0]

    isEnd,data = recievePacket(radio2,pipe)
    print(bcolors.OKGREEN,"[*] Packet ",str(c)," recieved",bcolors.ENDC)
    print(bcolors.OKBLUE,"[*] File length: "+''.join(chr(x) for x in data),bcolors.ENDC)
    c = c + 1

    while True:   
        isEnd,data = recievePacket(radio2,pipe)
        if isEnd:
            print(bcolors.OKGREEN,"[*] Transmission ended! Recieved file stored in ./text.txt",bcolors.ENDC)
            break
        if data!= False:
            print(bcolors.OKGREEN,"[*] Packet ",str(c)," recieved",bcolors.ENDC)
            c = c + 1
            text = ''.join(chr(x) for x in data)
            file.write(text)
        else:
            print(bcolors.FAIL,"[*] The recieved packet is corrupted",bcolors.ENDC)

def recievePacket(radio,pipe):
    while not radio.available(pipe):
        time.sleep(1/1000000)
    data = []
    radio.read(data,radio2.getDynamicPayloadSize())
    messageData = data[1:len(data)]
    isEnd,nextACKData = getSequenceNumber(data)
    
    if nextACKData != False:
        dataToSend = bytearray()
        dataToSend.extend(nextACKData)
        dataToSend.extend([0])
        sendACK(radio,dataToSend)
        return isEnd,data
    else:
        return False,False

def getSequenceNumber(data): 
    lastACKData = data[0]
    if lastACKData == 2:
        return False,[struct.pack("B",3)]
    elif lastACKData == 0:
        return False,[struct.pack("B",1)]
    elif lastACKData == 4:
        return True,[struct.pack("B",4)]
    return False,False

def sendACK(radio,nextACKData):
    radio.stopListening()
    radio.write(nextACKData)
    radio.startListening()
    print(bcolors.OKBLUE,"[*] ACK send",bcolors.ENDC)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
