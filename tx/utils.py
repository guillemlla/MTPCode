#MTP 2019 Quick Mode sender script.

from __future__ import print_function
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import spidev
import os
import struct

payload_size=32

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

#Radio Address and Init
def radio_init():
    radio = NRF24(GPIO, spidev.SpiDev())
    print("[*] Starting Radio Interface...")

    radio.begin(0, 25)
    radio.setPayloadSize(payload_size)
    radio.setChannel(0x60)
    radio.setDataRate(NRF24.BR_250KBPS)
    radio.setPALevel(NRF24.PA_LOW)
    radio.setAutoAck(True)
    radio.setRetries(15,15)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[0])
    radio.startListening()
    radio.stopListening()
    radio.printDetails()



