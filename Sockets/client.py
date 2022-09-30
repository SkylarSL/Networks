from email import message
from operator import mod
import sys
from socket import *

# accept commandline arguments and assigne them
serverName = str(sys.argv[1])
nPort = int(sys.argv[2])
reqCode = int(sys.argv[3])
messages = sys.argv[4:]


# TCP connection
# initiate a socket
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, nPort))
clientSocket.send(str(reqCode).encode())

rPort = int(clientSocket.recv(1024).decode())

if(rPort == -1):
    print("request codes do not match")
    exit(1)


# UDP
i = 0
while((i < len(messages)) | True):

    if(i >= len(messages)):
        message = input()
        print(message)
    if(i < len(messages)):
        message = messages[i]

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(message.encode(), (serverName, rPort))
    if(message == "EXIT"):
        clientSocket.close()
        break
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())

    i += 1
