#MTP 2019 Quick Mode Sender Group C

from utils_tx import send_data
from lib_nrf24 import NRF24

payload_size = 32
numPaquetesTx = 0
path = "text2send"
ch = 0x60
retry = (0,0)
begin = (0,25)
timeout = 5 #In seconds

#Radio Address and Init
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

send_data(path=path, numPaquetesTx= numPaquetesTx, payload_size= payload_size, datarate=NRF24.BR_250KBPS, palevel=NRF24.PA_MIN,\
pipe=pipes, autrotrack=False, channel=ch, retries=retry, begin=begin, timeout=timeout)
