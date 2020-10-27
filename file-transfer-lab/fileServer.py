#! /usr/bin/env python3

import socket, sys, re
sys.path.append("../lib")       # for params
import params
     # Symbolic name meaning all available interfaces


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 50001))
server.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets
loop = True

while loop:
    conn, addr = server.accept()  # wait until incoming connection request (and accept it)
    serverFile = 'receivingFile.txt'
    print('Connection established')

    with open(serverFile, 'wb') as fr:

        while 1:

            data = conn.recv(32)

            if data == b'Transfer complete':
                loop = False
                break

            else:
                fr.write(data)

    fr.close()

server.close()