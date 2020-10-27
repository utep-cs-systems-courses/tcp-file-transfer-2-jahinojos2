#! /usr/bin/env python3

import socket, sys, re, os, threading
sys.path.append("../lib")       # for params
import params


switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)
os.chdir("Server")

from threading import Thread

from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self):
        while True:
            file = (self.fsock.receive(debug)).decode()
            fileName, fileSize = file.split(":")
            fileSize = int(fileSize)
            if fileSize == 0:
                print("This is an empty file")
                sys.exit(1)
            if(os.path.isfile(fileName)):
                print("This is an exisiting file")
                sys.exit(1)
            lock = threading.Lock()
            with lock:
                with open(fileName, "w+b") as newFile:
                    count = 0
                    while count < fileSize:
                        payload = self.fsock.receive(debug)
                        data = bytes(payload)

                        if payload ==b'':
                            break
                        newFile.write(data)
                        count += 1
            newFile.close()
            if debug: print("rec'd: ", payload)
            if payload == b'':
                print("File received")
            sys.exit(0)
while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()