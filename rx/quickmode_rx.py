#MTP 2019 Quick Mode Receiver. Group 3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import utils

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
"""
radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(0, 25)

radio2.setRetries(15,15)

radio2.setPayloadSize(32)
radio2.setChannel(0x60)
radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_HIGH)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()

radio2.printDetails()

radio2.startListening()

"""
print("\n\n\n\n*****Quick mode*****\n\nWaiting for data...")

radio2=utils.init_radio()

c=1

file = open("text.txt", "w")
akpl_buf =[c,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8]
pipe = [0]

while not radio2.available(pipe):
    time.sleep(1000/1000000)

file_len = []
radio2.read(file_len,radio2.getDynamicPayloadSize())
print("File length: "+''.join(chr(x) for x in file_len))

radio2.writeAckPayload(1, akpl_buf,len(akpl_buf))

while True:
    while not radio2.available(pipe):
        time.sleep(10000/1000000.0)

    recv_buffer = []
    radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
    print (str(c)+" new message/s")
    c = c + 1
    text = ''.join(chr(x) for x in recv_buffer)

    if(''.join(chr(x) for x in recv_buffer)=="END"):
	radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
	print("Transmission ended! File is stored in ./text.txt")
        break
    file.write(text)
    radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
