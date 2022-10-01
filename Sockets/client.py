from email import message
from operator import mod
import sys
from socket import *

# accept commandline arguments and assigne them
serverName = str(sys.argv[1])
nPort = int(sys.argv[2])
reqCode = int(sys.argv[3])
messages = sys.argv[4:]
messages.append("EXIT")

# TCP

# initiate a TCP connection
tcpClientSocket = socket(AF_INET, SOCK_STREAM)

# connect to the server on the specified nPort (specified by the server)
tcpClientSocket.connect((serverName, nPort))
# send the request code for the server to verify
tcpClientSocket.send(str(reqCode).encode())

# retrieve the rPort (or error) from the server 
rPort = int(tcpClientSocket.recv(1024).decode())

# if rPort is -1, requests codes do not match, give error message and exit gracefully
if(rPort == -1):
    print("request codes do not match")
    exit(1)

tcpClientSocket.close()

# UDP

# instantiate a UDP connection
udpClientSocket = socket(AF_INET, SOCK_DGRAM)

# index variable for commandline messages
i = 0
while(True):

    # if i is more or equal to length of messages array then take input from 
    # commandline (used for EXIT, or other message inputs)
    if(i >= len(messages)):
        message = input()
        print(message)
    # if i is less than the length of messages array then take from the array
    if(i < len(messages)):
        message = messages[i]

    # send the client's message to the server
    udpClientSocket.sendto(message.encode(), (serverName, rPort))
    # if message is EXIT close the connection and break the loop and end the 
    # client program
    if(message == "EXIT"):
        break
    # recieve the message and server address from the server
    modifiedMessage, serverAddress = udpClientSocket.recvfrom(2048)
    # print the messages on the client side
    print(message)
    print(modifiedMessage.decode())

    # increment index variable
    i += 1
