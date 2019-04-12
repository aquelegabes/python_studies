import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command): #(1)
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/USER/.ssh/known_hosts') #(2)
    client.connect(ip,username=user,password=passwd) #(3)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print (ssh_session.recv(1024))
    return

ssh_command('127.0.0.1', 'user', 'pass', 'cls')