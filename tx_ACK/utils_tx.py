from __future__ import print_function
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import spidev
import time
import os
import struct

radio = NRF24(GPIO, spidev.SpiDev())

def init_radio(payload, datarate, palevel, pipe, autrotrack, channel, retries, begin):
    print("[*] Starting Radio Interface...")

    radio.begin(begin[0], begin[1])
    radio.setRetries(retries[0],retries[1])
    radio.setPayloadSize(payload)
    radio.setChannel(channel)
    radio.setDataRate(datarate)
    radio.setPALevel(palevel)
    radio.setAutoAck(autrotrack)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openWritingPipe(pipe[0])
    radio.openReadingPipe(1, pipe[1])
    radio.startListening()
    radio.stopListening()
    radio.printDetails()

def send_data(path, numPaquetesTx, payload_size, datarate, palevel, pipe, autrotrack, channel, retries, begin, timeout):
    payload_toSend = payload_size - 1
    file_len,text,file_pointer = readText(path,file,payload_toSend)

    lastSend = 0#0-> Not send or Validated 1-> Send
    numPacket = 0

    if(path!=0 and file!=""):

        init_radio(payload_size, datarate, palevel, pipe, autrotrack, channel, retries, begin)

    	time.sleep(10/1000)
	s = str(file_len)
	b = bytearray()
	b.extend(s)
	lastSend,numPacket = sendPacket(radio,b,timeout,lastSend,pipe,numPacket)
    	
    	while True:
    		time.sleep(1)
    		lastSend,numPacket = sendPacket(radio,text,timeout,lastSend,pipe,numPacket)
    	        time.sleep(10/1000)	
    		numPaquetesTx += 1
    		text = file_pointer.read(payload_toSend)

    		if text == '':
                        time.sleep(1)
    			lastSend,numPacket = sendPacket(radio,text,timeout,9,pipe,numPacket) #lastSend = 9 end transmition
    			radio.end()
    			print(bcolors.OKGREEN,"[*] Transmission Ended",bcolors.ENDC)
                        break
    else:
        print("[*] File Not Found")

def readText(path,file,payload_toSend):
    for file in os.listdir(path):

        if file.endswith(".txt"):
            file_path = os.path.join(path, file)
            file_pointer = open(file_path, 'r')
            file_len = os.path.getsize(file_path)
            text = file_pointer.read(payload_toSend)
            byte_text = bytearray(text)
            return file_len,byte_text,file_pointer
    return 0,"","";

#The first byte will correspond to headers
#xy000000
#x-> 0 if not ACK 1 if ack
#y-> number of packet 0 or 1
#00:0-> no ACK packet 0 01:1->ACK packet 0
#10:2->no ACK packet 1 11:3 -> ACK packet 1
#100:4 -> End transmition
def sendPacket(radio,data,timeout,lastSend,pipe,numPacket):

    send = False
    while not send:
        lastSend,nextSequenceNumber = nextSequenceNumbers(lastSend,False) 
	dataToSend = bytearray()
	dataToSend.extend(nextSequenceNumber)
	dataToSend.extend(data)
        send,numPacket = sendData(radio,dataToSend,timeout,lastSend,pipe,numPacket)
    return lastSend,numPacket

def nextSequenceNumbers(lastSend,isACK):
    
    if lastSend==0 and not isACK:
        lastSend = 2
        return lastSend,[struct.pack("B",2)]
    elif lastSend==2 and isACK:
        return lastSend,3
    elif lastSend==2 and not isACK:
        lastSend = 0
        return lastSend,[struct.pack("B",0)]
    elif lastSend==0 and isACK:
        return lastSend,1 
    elif lastSend == 9 and not isACK:
        return lastSend,[struct.pack("B",4)]
    elif lastSend == 9  and isACK:
        return lastSend,4

def sendData(radio,data,timeout,lastSend,pipe,numPacket):

    radio.stopListening()
    radio.write(data)
    print(bcolors.OKBLUE, "[*] Packet ",numPacket," Send",bcolors.ENDC)
    radio.startListening()
    
    start = time.time()
    file = [-1]
    notImportant,nextSequenceNumber = nextSequenceNumbers(lastSend,True)
    while file[0] != nextSequenceNumber:
        while not radio.available(pipe):
            time.sleep(1000/1000000)
            if isTimeout(start,timeout):
                print(bcolors.FAIL,"[*] Packet ",numPacket," Timeout",bcolors.ENDC)
                return False,numPacket
        file = []
        radio.read(file,radio.getPayloadSize())
    
    print(bcolors.OKGREEN,"[*] ACK ",numPacket," recived",bcolors.ENDC)
    numPacket = numPacket + 1
    return True,numPacket

def isTimeout(startTime,timeout):
    end = time.time()
    if (end-startTime)>timeout:
        return True
    return False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
