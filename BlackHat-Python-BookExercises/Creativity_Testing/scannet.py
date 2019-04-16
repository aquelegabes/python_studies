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

    # we'll assume it's only going to be 2 lines for windows
    if os.name == "nt": #windows
        call('ipconfig | findstr -i ipv4 > ipv4.txt', shell=True)
        call('ipconfig | findstr -i sub > subnet.txt', shell=True)
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
    else:
    # and in one line we can get the info we want in linux/mac
        
        call('ifconfig | grep -i inet > ipv4.txt', shell=True)
        file = open("ipv4.txt", "r")
        inets = []

        for line in file:
            inets.append(line)
            break
        file.close()
        call('rm -rf ipv4.txt', shell=True)
        
        inets = inets[0].strip().split(' ')
        inets = filter(lambda net: len(net) > 1 and net.__contains__('.'), inets)
        # assuming we did it right
        # [0] myhost, [1] subnet, [2] broadcast
        localhost = inets[0]
        subnet = inets[1]
        
        
    return localhost, subnet

def scanning():
    host, subnet = getHosts()
    print host,subnet
    

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
                        "hle:t:p:c",
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
        elif options in ("-udp"):
            typeconn = socket.SOCK_DGRAM
        elif options in ("-tcp"):
            typeconn = socket.SOCK_STREAM
        else:
            assert False,"Opção inválida"

    if listen and len(target) and port > 0:
        if not len(typeconn):
            typeconn = "TCP"
        
        if len(sender):
            connecting(target,port,typeconn,sender)
        else:
            listening(target,port,typeconn)

main()