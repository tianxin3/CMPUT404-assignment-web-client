#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from urllib.parse import urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):


    def get_host_port(self,url):

        urlContent = urllib.parse.urlparse(url)
        host = urlContent.hostname
        port = urlContent.port

        if port == None:
            port = 80

        return host, port

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        statusLine = data.split("\r\n")[0]
        statusCode = statusLine.split(" ")[1]
        return int(statusCode)

    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # code = 500
        # body = ""

        # Get host&port and connect to it
        host, port = self.get_host_port(url)
        self.connect(host, port)

        # Send GET request
        request_content = "GET {0} HTTP/1.1\r\nHost: {1}\r\nConnection: close\r\n\r\n".format(url, host)
        self.sendall(request_content)

        # Get response
        response_content = self.recvall(self.socket)
        print(response_content)
        code = self.get_code(response_content)
        body = self.get_body(response_content)
        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # code = 500
        # body = ""

        # Get host&port and connect to it
        host, port = self.get_host_port(url)
        self.connect(host, port)

        # Encode body
        if args != None:
            encode_args = urlencode(args)
        else:
            encode_args = ""
        args_length = len(encode_args)

        # Send POST request
        request_content = "POST {0} HTTP/1.1\r\nHost: {1}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length:{2}\r\nConnection: close\r\n\r\n{3}".format(url, host, args_length, encode_args)
        self.sendall(request_content)

        # Get response
        response_content = self.recvall(self.socket)
        print(response_content)
        code = self.get_code(response_content)
        body = self.get_body(response_content)
        self.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
