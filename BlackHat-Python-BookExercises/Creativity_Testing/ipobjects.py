# -*- coding: utf-8 -*-

import socket
import struct
from ctypes import Structure, c_ubyte, c_ushort, c_ulong

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

class ICMP(Structure): #(1)
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

def SocketTCP():
    return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def SocketUDP():
    return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

