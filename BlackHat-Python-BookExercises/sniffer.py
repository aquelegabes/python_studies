import socket
import os

# host que ouvirá
host = "10.170.68.217" # eu msm

# cria um host puro e associa-o a interface publica

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP # (1)
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((host, 0))

# queremos cabeçalhos IP incluidos na captura
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1) # (2)

# se estivermos usando WIndows, enviar um IOCTL
# configurar modo promíscuo 
if os.name == "nt": #(3)
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

# lê um pacote unico
print(sniffer.recvfrom(65565)) #(4)

# se estivermos usando Windows, desabilitar modo promiscuo

if os.name == "nt": #(5)
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)