from network import LoRa
import socket
import machine
import time

lora = LoRa(mode=LoRa.LORA, region=LoRa.US915)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

while True:
    s.setblocking('Hello')
    s.send('Hello')

    s.setblocking(False)
    data = s.recv(64)
    print(data)

    time.sleep(machine.rng() & 0x0F)