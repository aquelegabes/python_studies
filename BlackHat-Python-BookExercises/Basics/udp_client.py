# -*- coding: utf-8 -*-

import socket

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 80

#criando objeto socket
#AF_INET = IPv4
#SOCK_DGRAM = cliente UDP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#enviando alguns dados
#b = transformar em bytes
client.sendto(b"AAABBBCCC",(TARGET_HOST,TARGET_PORT))

#recebendo dados
#obs: em um cliente UDP recebe tanto os dados
#quanto os detalhes do host remoto e a porta
data, addr = client.recvfrom(4096)

print(data)