""" 
    CES-35 - Redes de Computadores
    Laboratório 1 - Sockets
    Nicholas Scharan Cysne (PMG)

    response.py
"""

import json

class Response:
    def __init__(self, obj=dict()) -> None:
        self.status = obj.get("Status", "400") 
        self.status_msg = obj.get("State Message", "Bad Request")
        self.content = obj.get("Content", "")
        self.content_type = obj.get("Content-Type", "text/html")
        self.version = obj.get("Version", "HTTP/1.0")

    def encode(self):
        msg = " ".join([self.version, self.status, self.status_msg])
        msg += "\r\n" + f"Content-Length: {len(self.content)}"
        msg += "\r\n" + "Connection: Closed"
        msg += "\r\n" + "Content-Type: text/html; charset=utf-8"
        msg += "\r\n\r\n" + self.content
        msg += "\r\n\r\n"

        # Convert to bytes
        return bytes(msg, encoding='utf-8') 

    def parse(byteObj):
        res = dict()
        # Decode byte object
        msg = byteObj.decode('utf-8')
        # Separate field in HTTP Response
        obj = msg.split("\r\n")
        # Retrieve information from HTTP Response
        header = obj[0].split(" ")
        res["Version"] = header[0]
        res["Status"] = header[1]
        res["Status Message"] = header[2]
        # get Content-Type
        content_type = obj[3].split(" ")
        res["Content-Type"] = content_type[1] + " " + content_type[2]
        res["Content"] = obj[5]
        # Return Response object
        return Response(res)

    def set_status(self, status):
        self.status = status
        if status == "200":
            self.status_msg = "OK" 
        if status == "400":
            self.status_msg = "Bad Request" 
        if status == "404":
            self.status_msg = "Not Found" 

    def set_content(self, content):
        self.content = content
        self.content_type = "text/html"

