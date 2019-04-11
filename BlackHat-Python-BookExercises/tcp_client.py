import socket

TARGET_HOST = "www.google.com"
TARGET_PORT = 80

#criando objeto socket
#AF_INET = IPv4
#SOCK_STREAM = cliente TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#fazendo cliente conectar-se
client.connect((TARGET_HOST,TARGET_PORT))

#enviando alguns dados
#b = transformar em bytes
client.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")

#recebendo dados
response = client.recv(4096)

print(response)