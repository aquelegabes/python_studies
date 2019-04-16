# -*- coding: utf-8 -*-

import sys
import os
import socket
import getopt
import time
from threading import Thread
from ipobjects import IP, ICMP
from netaddr import IPNetwork, IPAddress
from subprocess import call

# globals
listen = False
connect = False
sender = ""
target = ""
typeconn = ""
port = int()
message = "checkIfAlive!"

def help():
    print (u"ScanNet -- Scan, listen, connect")
    print (u"-s --scan \t\tEscaneia a rede para entradas de hosts")
    print (u"-t --target \t\tDefine um alvo. ex: -t 192.168.1.21")
    print (u"-p --port \t\tDefine uma porta. ex: -p 53125")
    print (u"-l --listen \t\tEscutar na conexão padrão TCP")
    print (u"-c --connect \t\tConecta e envia algo na conexão padrão TCP. ex: -c 123feijaoarroz")
    print (u"-udp \t\t\tDefine porta UDP para conexão")
    print (u"-tcp \t\t\tDefine porta TCP para conexão")
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

def udp_sender(subnet,msg):
    time.sleep(2)
    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(msg.encode('utf8'),(("%s") % ip,65212))
            # print "[*] Sent to => %s:65212" % (ip)
        except:
            # print "[*] Failed sending to => %s:65212" % (ip)
            pass

def scanning():
    host, subnet = getHosts()
    hostsplit = host.split('.')
    hostsplit[-1] = "0"
    defaulthost = "%s.%s.%s.%s" % (hostsplit[0], hostsplit[1], hostsplit[2], hostsplit[3])
    # set default subnet as 255 max hosts
    subnet = "%s/22" % (defaulthost)
    
    t = Thread(target=udp_sender, args=(subnet,message))
    t.start()

    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    scanner = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
    scanner.bind((host, 0))
    scanner.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
    if os.name == "nt":
        scanner.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = scanner.recvfrom(65565)[0]
            ip_header = IP(raw_buffer[0:20])

            if ip_header.protocol == "ICMP":
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset : offset + sys.getsizeof(ICMP)]
                icmp_header = ICMP(buf)

                if icmp_header.code == 3 and icmp_header.type == 3:
                    if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                        if raw_buffer[len(raw_buffer)-len(message):] == message:
                            print("[*] Host Up: %s" % ip_header.src_address)

                continue

    except KeyboardInterrupt:
        if os.name == "nt":
            scanner.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
        print "\n[*] Exiting..."
        sys.exit(0)

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
                        "hlcsut:p:t",
                        ["help", "listen", "target=", "port=", "connect", "scan", "udp", "tcp"])
    except getopt.GetoptError as err:
        print (str(err))
        print
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