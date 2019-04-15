# -*- coding: utf-8 -*-
''' definindo caracteres UTF8 '''

import socket
import os
import struct
import threading
import sys
import time
from netaddr import IPNetwork, IPAddress
from ctypes import c_ubyte,c_ushort,c_ulong,Structure

# host que ouvira
HOST = "10.170.68.217"

# sub rede
SUBNET = "10.170.68.0/22"

# string mágica em relacao a qual verificaremos as respostas ICMP
MAGIC_STRING = "PYTHONRULES!" #(1)

# este codigo espalha os datagramas UDP
def udp_sender(subnet, msg): #(2)
    time.sleep(5)
    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):
        try:
            sender.sendto(msg,("%s") % ip,65212)
        except:
            pass

class ICMP(Structure):
	_fields_ = [
		("type",        c_ubyte),
		("code",        c_ubyte),
		("checksum",    c_ushort),
		("unused",		c_ushort),
		("next_hop_mtu",c_ushort)
	]

	def __new__(self, socket_buffer):
		return self.from_buffer_copy(socket_buffer)
	
	def __init__(self, socket_buffer):
		pass

# nosso cabecalho IP
class IP(Structure):
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

        # enderecos IP legiveis
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        # protocolo legivel
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

# codigo visto no exemplo sniffer.py

# comeca a enviar pacotes
t = threading.Thread(target=udp_sender, args=(SUBNET,MAGIC_STRING))
t.start()

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
        raw_buffer = sniffer.recvfrom(65565)[0]

        # criando cabecalho IP a partir dos 20 primeiros bytes do buffer
        ip_header = IP(raw_buffer[0:20])

        # exibe protocolo detectado e os hosts
        #print ("Protocolo : %s De: %s -> Para: %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
        
		# se for ICMP, nos queremos o pacote
        if ip_header.protocol == "ICMP": #(2)
            # calcula em que ponto nosso pacote ICMP comeca
            offset = ip_header.ihl * 4 #(3)
            buf = raw_buffer[offset : offset + sys.getsizeof(ICMP)]

            # cria nossa estrutura ICMP
            icmp_header = ICMP(buf) #(4)

            #print ("ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code))
            # verifica se type e code sao iguais a 3
            if icmp_header.code == 3 and icmp_header.type == 3:
                
                # garantir que o host esta em nossa sub-rede
                if IPAddress(ip_header.src_address) in IPNetwork(SUBNET):

                    # garante que contem nossa mensagem
                    if raw_buffer[len(raw_buffer)-len(MAGIC_STRING):] == MAGIC_STRING:
                        print("Host Up: %s" % ip_header.src_address)

# tratando ctrl-c
except KeyboardInterrupt:
    # se usando Windows, desabilitar modo promiscuo
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
    print ("Exiting...")
    sys.exit(0)