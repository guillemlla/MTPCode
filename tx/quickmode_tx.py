#MTP 2019 Quick Mode sender script.

from __future__ import print_function
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import spidev
import time
import os
import struct
import utils

payload_size=32
path = "test"
numPaquetesTx=1

#Radio Address and Init
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())

def radio_init():

    print("[*] Starting Radio Interface...")

    radio.begin(0, 25)
    radio.setPayloadSize(payload_size)
    radio.setChannel(0x60)
    radio.setDataRate(NRF24.BR_250KBPS)
    radio.setPALevel(NRF24.PA_HIGH)
    radio.setAutoAck(True)
    radio.setRetries(15,15)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[0])
    radio.startListening()
    radio.stopListening()
    radio.printDetails()

utils.radio_init()

for file in os.listdir(path):

    if file.endswith(".txt"):

	file_path = os.path.join(path, file)
        file_pointer = open(file_path, 'r')
	file_len = os.path.getsize(file_path)
        radio_init()
	text = file_pointer.read(payload_size)
	time.sleep(10/1000)
	radio.write(str(file_len))
	time.sleep(10/1000)

	while True:
		time.sleep(10/1000.0)
		radio.write(text)
		time.sleep(1000/1000)

		print("[*]",numPaquetesTx)

		ack_buffer = []
		radio.read(ack_buffer, radio.getDynamicPayloadSize())
		numPaquetesTx += 1
		text = file_pointer.read(payload_size)

		if text == '':
			print("[*] Ended")
			print("[*] Packets sent:", numPaquetesTx)

			radio.write("END")
			radio.end()

    			break
