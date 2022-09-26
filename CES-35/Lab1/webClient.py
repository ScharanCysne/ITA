""" 
    CES-35 - Redes de Computadores
    Laboratório 1 - Sockets
    Nicholas Scharan Cysne (PMG)

    webClient.py
"""

import sys

from socket  import *
from request import Request
from response import Response

DIR = "webClient"

def __main__():
    # Get list of urls passed as argument
    urls = sys.argv[1:]

    # For each url, parse request, send request to local webserver, receive response
    for url in urls:
        obj = Request.parseURL(url)

        # Get Address and Port numver for TCP connection 
        addr = obj["addr"]
        port = obj["port"]
        # Create TCP socket on client to use for connecting to remote
        # server.  Indicate the server's remote listening port
        # Error in textbook?   socket(socket.AF_INET, socket.SOCK_STREAM)  Amer 4-2013 
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # Open the TCP connection
        clientSocket.connect((addr,int(port)))

        # Create HTTP Request
        r = Request(obj)
        # Serialize request
        data = r.encode()
        # Output to console what is sent to the server
        print("Sent to Web Server: ", data)
        # Send serialize request over the TCP connection
        clientSocket.send(data)
        
        # Get response by the server
        resp = clientSocket.recv(1024)
        response = Response.parse(resp)
        # Output response 
        print("Response: ", resp)
        # Save in WebClient directory
        if response.status == "200":
            if r.url == "/":
                with open(DIR + "/index.html", 'w') as f:
                    f.write(response.content)
            else:
                with open(DIR + r.url, 'w') as f:
                    f.write(response.content)

        # close the TCP connection
        clientSocket.close()


if __name__ == "__main__":
    __main__()