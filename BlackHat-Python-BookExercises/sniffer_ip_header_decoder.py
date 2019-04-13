# -*- coding: utf-8 -*-

import socket
import os
import struct
from ctypes import c_ubyte,c_ushort,c_ulong,Structure

# host que ouvirá
HOST = "10.170.68.217"

# nosso cabeçalho IP
class IP(Structure): #(1)
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_ulong),
        ("dst",             c_ulong)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffet=None):
        # mapeia constantes do protocolo aos seus nomes
        self.protocol_map = {1:"ICMP",6:"TCP", 17:"UDP"}

        # endereços IP legíveis #(2)
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        # protocolo legível
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

# código visto no exemplo sniffer.py
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((HOST, 0))

sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

try:
    while True:
        # lendo pacote
        raw_buffer = sniffer.recvfrom(65565)[0] #(3)

        # criando cabecalho IP a partir dos 20 primeiros bytes do buffer
        ip_header = IP(raw_buffer[0:20]) #(4)

        #exibe protocolo detectado e os hosts
        print ("Protocolo : %s De: %s -> Para: %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)) #(5)
#tratando ctrl-c
except KeyboardInterrupt:
    #se usando Windows, desabilitar modo promiscuo
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)