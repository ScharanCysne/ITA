""" 
    CES-35 - Redes de Computadores
    Laboratório 1 - Sockets
    Nicholas Scharan Cysne (PMG)

    request.py
"""

import json

from socket import gethostbyname

class Request:
    def __init__(self, obj=dict()) -> None:
        self.version = obj.get("version", "HTTP/1.0")
        self.host = obj.get("host","")
        self.port = obj.get("port","")
        self.url = obj.get("url", "/")
        self.method = obj.get("method","GET")

    def encode(self):
        msg = " ".join([self.method, self.url, self.version])
        msg += "\r\n" + "Host: " + self.host + ":" + self.port
        msg += "\r\n" + "Accept: text/html"
        msg += "\r\n\r\n"
        # Convert to bytes
        return bytes(msg, encoding='utf-8') 

    def parse(byteObj):
        req = dict()
        # Decode byte object
        msg = byteObj.decode('utf-8')
        # Separate field in HTTP Request 
        obj = msg.split("\r\n")
        # Retrieve information from HTTP Request
        header = obj[0].split(" ")
        req['method'] = header[0]
        req['url'] = header[1]
        req['version'] = header[2]
        host_info = obj[1].split(" ")
        destination = host_info[1].split(":")
        req['host'] = destination[0]
        req['port'] = destination[1]

        # Return Request object
        return Request(req)

    def parseURL(url):
        # Split http://host:port/file into ["http:","","host","port","file"] 
        s = url.split("/")
        # Split host:port
        destination = s[2].split(":")
        host = destination[0].replace("www.","")
        port = destination[1]
        file = s[3]

        return {
            'host': host,                   # Host Name
            'addr': gethostbyname(host),    # Host IP Address
            'port': port,                   # Port Number
            'url': "/" + file               # File of interest
        }