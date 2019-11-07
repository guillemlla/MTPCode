#MTP 2019 Quick Mode Receiver. Group 3

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

def init_radio():
	radio2 = NRF24(GPIO, spidev.SpiDev())
	radio2.begin(0, 25)

	radio2.setRetries(15,15)

	radio2.setPayloadSize(32)
	radio2.setChannel(0x60)
	radio2.setDataRate(NRF24.BR_250KBPS)
	radio2.setPALevel(NRF24.PA_LOW)

	radio2.setAutoAck(True)
	radio2.enableDynamicPayloads()
	radio2.enableAckPayload()

	radio2.openWritingPipe(pipes[0])
	radio2.openReadingPipe(1, pipes[1])

	radio2.startListening()
	radio2.stopListening()

	radio2.printDetails()

	radio2.startListening()
	return radio2
