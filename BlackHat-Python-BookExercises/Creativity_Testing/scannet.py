''' #!/usr/bin/python '''
# -*- coding: utf-8 -*-

import ipobjects
import sys
import os
import socket
import getopt
from subprocess import call

# globals
listen = False
connect = False
sender = ""
target = ""
typeconn = ""
port = int()

def help():
    print ("ScanNet -- Scan, listen, connect")
    print ("-s --scan \tEscaneia a rede para entradas de hosts")
    print ("-t --target \tDefine um alvo. ex: -t 192.168.1.21")
    print ("-p --port \tDefine uma porta. ex: -p 53125")
    print ("-l --listen \tEscutar na conexão padrão TCP")
    print ("-c --connect \tConecta e envia algo na conexão padrão TCP. ex: -c 123feijaoarroz")
    print ("-udp \tDefine porta UDP para conexão")
    print ("-tcp \tDefine porta TCP para conexão")
    sys.exit(0)

def getHosts():
    ipv4s = []
    subnets = []

    if os.name == "nt": #windows
        call('ipconfig | findstr -i ipv4 > ipv4.txt', shell=True)
        call('ipconfig | findstr -i sub > subnet.txt', shell=True)

    # we'll assume it's only going to be 2 lines
    file = open("ipv4.txt", "r")

    for line in file:
        ipv4s.append(line),
    file.close()
    call('rm -f ipv4.txt', shell=True)
    localhost = ipv4s[1].split(' ')[-1].replace('\n', '')

    file = open("subnet.txt", "r")

    for line in file:
        subnets.append(line)
    file.close()
    call('rm -rf subnet.txt', shell=True)
    subnet = subnets[1].split(' ')[-1].replace('\n', '')

    return localhost, subnet

def scanning():
    host, subnet = getHosts()
    

def listening(target,port,typeconn):
    print()

def connecting(target,port,typeconn,sender):
    print()

def main():
    global listen
    global port
    global target
    global connect
    global sender
    global typeconn

    if not len(sys.argv[1:]):
        help()
    
    try:
        opts, args = getopt.getopt(
                        sys.argv[1:],
                        "hle:t:p:cu",
                        ["help", "listen", "target", "port", "connect", "scan", "udp", "tcp"])
    except getopt.GetoptError as err:
        print (str(err))
        help()

    for options,argument in opts:
        if options in ("-h", "--help"):
            help()
        elif options in ("-s", "--scan"):
            scanning()
        elif options in ("-l", "--listen"):
            listen = True
        elif options in ("-c","--connect"):
            connect = True
            sender = argument
        elif options in ("-t", "--target"):
            target = argument
        elif options in ("-p", "--port"):
            port = int(argument)
        elif options in ("-udp", "-tcp"):
            typeconn = argument
        else:
            assert False,"Opção inválida"

    if listen and len(target) and port > 0:
        if not len(typeconn):
            typeconn = "TCP"
        
        if len(sender):
            connecting(target,port,typeconn,sender)
        else:
            listening(target,port,typeconn)