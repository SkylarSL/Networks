import sys
from socket import *

# function to get a TCP socket
def getTCPConnection(serverName):
    # instantiate a socket for TCP 
    tcpServerSocket = socket(AF_INET, SOCK_STREAM)
    # bind the socket to 127.0.0.1 and let it pick an open port
    tcpServerSocket.bind((serverName, 0))
    return tcpServerSocket

# function to get a UDP socket
def getUDPConnection(serverName):
    # instantiate a UDP connection
    udpServerSocket = socket(AF_INET, SOCK_DGRAM)
    # bind to an addr and open port
    udpServerSocket.bind((serverName, 0))
    return udpServerSocket

# check number of arguments
if(len(sys.argv) < 2 or len(sys.argv) > 2):
    print("incorrect number of arguments")
    exit(1)
# get the request code from input
try:
    reqCode = int(sys.argv[1])
except:
    print("reqCode is not an integer")
    exit(1)

# server name, must be a string
serverName = ""
# check if server name is a string
if(type(serverName) != str):
    print("server name must be a string")
    exit(1)

# instantiate a socket for TCP 
tcpServerSocket = getTCPConnection(serverName)

# get the port the socket chose, this is nPort
nPort = tcpServerSocket.getsockname()[1]

# let the socket start listening
tcpServerSocket.listen(1)

# let the client know (in terminal) that the server is listening on nPort
print("TCP ready to serve")
print("SERVER_PORT="+str(nPort))

while True:

    # wait for client connection
    connectionSocket, address = tcpServerSocket.accept()
    # recieve the request code from the client
    incomingReqCode = int(connectionSocket.recv(1024).decode())

    rPort = -1
    # if the request code does not match, close the socket and send an error message
    if(incomingReqCode != reqCode):
        # send error message
        connectionSocket.send(str(rPort).encode())
        # close the tcp connection
        connectionSocket.close()
    # if it does match set up a UDP connection and send back an rPort to make 
    # the subsequent requests
    else:
        # set up a UDP connection
        udpServerSocket = getUDPConnection(serverName)
        # get the rPort
        rPort = udpServerSocket.getsockname()[1]
        # send the rPort to the client
        connectionSocket.send(str(rPort).encode())

    # loop to recieve messages
    if(rPort != -1):
        while True:
            #recieve the message and address from the client
            message, clientAddress = udpServerSocket.recvfrom(2048)
            # decode the message
            message = message.decode()
            # if the message is exit then close the socket and start over
            if(message == "EXIT"):
                udpServerSocket.close()
                break
            # reverse the message
            modifiedMessage = message[::-1]
            # send the message back to the client
            udpServerSocket.sendto(modifiedMessage.encode(), clientAddress)
            
