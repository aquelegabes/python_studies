import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))
    except:
        print ("[!!] Failed to listen on %s:%d" % (local_host,local_port))
        print ("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    
    print ("[*] Listening on %s:%d" % (local_host,local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        ''' exibir informações sobre conexão local '''
        print ("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))

        ''' inicia uma thread para conversar com o host remoto '''
        proxy_thread = threading.Thread(target = proxy_handler, args= (client_socket, remote_host, remote_port, receive_first))

        proxy_thread.start()

def main():
    ''' sem parsing sofisticado de linha de comando nesse caso '''
    if len(sys.argv[1:]) != 5:
        print ("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefirst]")
        print ("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    ''' define parâmetros para ouvir localmente '''
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    ''' define alvo remoto '''
    remote_host = sys.argv[3]
    remote_port = sys.argv[4]

    ''' diz ao nosso proxy para conectar e receber dados '''
    ''' antes de enviar ao host remoto '''
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    
    ''' colocando em ação o socket que ficará ouvindo '''
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

main()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    ''' conecta-se ao host remoto '''
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    ''' recebe dados do lado remoto, se for necessário '''
    ''' (1) '''
    if receive_first: 
        ''' (2) '''
        remote_buffer = receive_from(remote_socket)
        ''' (3) '''
        hexdump(remote_buffer)

        ''' envia dados ao handler de resposta '''
        ''' (4) '''
        remote_buffer = response_handler(remote_buffer)
        
        ''' se houver dados para serem enviados ao cliente local, envia-os '''
        if len(remote_buffer):
            print ("[<==] Sendind %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)
    
    ''' entrar no laço e ler de local host '''
    ''' enviar para host remoto, enviar para host local '''
    ''' enxaguar lavar repetir (LUL) '''

    while True:
        ''' le do localhost '''
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)
            
            ''' envia os dados para nosso handler de solicitações '''
            local_buffer = request_handler(local_buffer)

            ''' envia dados para host remoto '''
            remote_socket.send(local_buffer)
            print ("[===>] Sent to remote.")
        
        ''' recebe resposta '''
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            ''' envia dados ao handler de resposta '''
            remote_buffer = response_handler(remote_buffer)

            ''' envia a resposta para o socket local '''
            client_socket.send(remote_buffer)

            print ("[<==] Sent to localhost.")
        
        ''' se não houver dados encerra conexão '''
        ''' (5) '''
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()

            print ("[*] No more data. Closing connections.")
            break

''' 
função de dumping de valores hexa diretamente obtida dos
comentários em
http://code.activestate.com/recipes/142812-hex-dumper
(1)
'''
def hexdump(src, length = 16):
    result = []
    digits = 4 if isinstance(src, str) else 2
    for i in range(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)

''' (2) '''
def receive_from(connection):
    buffer = ""

    '''
    definimos um temout de 2 segundos; de acordo com
    seu algo, pode ser que esse valor precise ser ajustado
    '''

    connection.settimeout(2)

    try:
        ''' 
        continua lendo em buffer até que não haja mais dados
        ou a temporização expire
        '''
        while True:
            data = connection.recv(4096)

            if not data:
                break
            
            buffer += data
    except:
        pass

    return buffer

''' (3) '''
def request_handler(buffer):
    ''' 
    possível fazer modificações no pacote
    '''
    return buffer

''' (4) '''
def response_handler(buffer):
    ''' 
    possível fazer modificações no pacote
    '''
    return buffer