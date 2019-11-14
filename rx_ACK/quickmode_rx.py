#MTP 2019 Quick Mode Receiver Group C

from utils_rx import init_radio, receive_data
from lib_nrf24 import NRF24

payload_size = 32
numPaquetesTx = 0
path = "text2send"
ch = 0x60
retry = (15,15)
begin = (0,25)

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

init_radio(payload=payload_size, datarate=NRF24.BR_250KBPS, palevel=NRF24.PA_MIN,\
pipe=pipes, autrotrack=True, channel=ch, retries=retry, begin=begin )

receive_data()
