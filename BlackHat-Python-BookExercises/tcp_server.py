import socket
import threading

BIND_IP = "0.0.0.0"
BIND_PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#dizendo ao servidor qual endereco ele deve ouvir
server.bind((BIND_IP,BIND_PORT))

#servidor comeca a ouvir
#maximo de conexoes acumuladas = 5
server.listen(5)

print ("[*] Listening on %s:%d" % (BIND_IP,BIND_PORT))

#esta eh a thread para tratamento de clientes

def handle_client(client_socket):
    #exibe o que o cliente quer enviar
    request = client_socket.recv(1024)
    print ("[*] Received: %s" % request)

    #envia o pacote de volta
    client_socket.send(b"ACK!")

    client_socket.close()

while True:
    #cliente conectado
    client, addr = server.accept()

    print ("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))

    #coloca a trhead de cliente em acaoo para tratar dados de entrada
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
