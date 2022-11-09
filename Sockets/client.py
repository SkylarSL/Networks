from email import message
import sys
from socket import *

def getTCPConnection(serverName, nPort):
    # initiate a TCP connection
    tcpClientSocket = socket(AF_INET, SOCK_STREAM)
    # connect to the server on the specified nPort (specified by the server)
    try:
        tcpClientSocket.connect((serverName, nPort))
    except:
        print("server name/address not known or wrong port")
        exit(1)
    return tcpClientSocket

# check for number of arguments
if(len(sys.argv) < 5):
    print("not enough arguments")
    exit(1)

# accept commandline arguments and assign them
serverName = sys.argv[1]
try:
    nPort = int(sys.argv[2])
except:
    print("nPort is not an integer")
    exit(1)
try:
    reqCode = int(sys.argv[3])
except:
    print("reqCode is not an integer")
    exit(1)
messages = sys.argv[4:]
messages.append("EXIT")
# check for correct input
if((type(serverName) != str or (type(nPort) != int) or (type(reqCode) != int) or (type(messages) != list))):
    print("incorrect client arguments")
    exit(1)

# make TCP connection
tcpClientSocket = getTCPConnection(serverName, nPort)
# send the request code for the server to verify
tcpClientSocket.send(str(reqCode).encode())

# retrieve the rPort (or error) from the server 
rPort = int(tcpClientSocket.recv(1024).decode())
# if rPort is -1, requests codes do not match, give error message and exit gracefully
if(rPort == -1):
    print("request codes do not match")
    exit(1)

# close the tcp connection after recieving rPort
tcpClientSocket.close()

# instantiate a UDP connection
udpClientSocket = socket(AF_INET, SOCK_DGRAM)

# index variable for commandline messages
i = 0
while(True):

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
    print(modifiedMessage.decode())

    # increment index variable
    i += 1
