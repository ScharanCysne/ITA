""" 
    CES-35 - Redes de Computadores
    Laboratório 1 - Sockets
    Nicholas Scharan Cysne (PMG)

    webServer.py
"""

import os
import sys
import threading

from socket import *
from request import Request
from response import Response

# Default directory for webServer
DIR = "webServer"

def processRequest(connectionSocket, addr):
    # Read a sentence of bytes from socket sent by the client
    data = connectionSocket.recv(1024)
    # Output to console the data received from the client 
    print ("Received From Client: ", data)
    
    # Parse request
    request = Request.parse(data)
    response = Response()

    # GET requested file
    if request.method == "GET":
        requestedUrl = request.url
        requestedFile = requestedUrl[1:] 
        # Check if file exists in directory
        if requestedUrl == "/" and "index.html" in os.listdir(DIR):
            response.set_status("200")
            with open(DIR + "/index.html", 'r') as f:
                response.set_content(f.read())
        elif requestedFile in os.listdir(DIR):
            response.set_status("200")
            with open(DIR + requestedUrl, 'r') as f:
                response.set_content(f.read())
        else:
            response.set_status("404")
    else:
        response.set_status("400")

    # Send response over the TCP connection
    connectionSocket.send(response.encode())
    
    # close the TCP connection; the welcoming socket continues
    connectionSocket.close()
        

def __main__():
    host = sys.argv[1]  # Host Name
    port = sys.argv[2]  # Host Port

    # Find IP address from host name
    addr = gethostbyname(host)
    
    # Create TCP welcoming socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind((addr, int(port)))

    # server begins listening for incoming TCP requests
    serverSocket.listen(1)

    # output to console that server is listening 
    print ("Web Server listening... ")
    # Forever listen for incoming requests     
    while 1:
        # Server waits for incoming requests
        connectionSocket, addr = serverSocket.accept()
        # Start new thread to process incoming request
        t = threading.Thread(target=processRequest, args=(connectionSocket, addr))
        t.start()

if __name__ == "__main__":
    __main__()