#! /usr/bin/env python3

import socket, sys, re

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("localhost", 50001))

sendFile = 'clientFile.txt'


with open(sendFile, 'rb') as fs:
    print('Sending file info')

    while True:
        dataTransfer = fs.read(1024)

        clientSocket.send(dataTransfer)

        if not dataTransfer:
            break

    clientSocket.send(b'Transfer complete')

clientSocket.close()