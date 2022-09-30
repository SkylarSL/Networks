import sys
from socket import *

# function to find an open port
def findPort():
    for port in range(1024, 65535):
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        test = s.connect_ex(("127.0.0.1", port))
        #print(test)
        if(test == 0):
            print(s)
            print("PORT: ", str(port))
            return port

while True:

    # TCP

    # get the request code from input
    reqCode = int(sys.argv[1])
    # get an open port
    nPort = findPort()
    # instantiate a socket for TCP 
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # bind the socket to a host and port
    serverSocket.bind(("127.0.0.1", nPort))
    # let the socket start listening?
    serverSocket.listen(1)
    # let the client know (in terminal) that the server is listening on nPort
    print("TCP ready to serve")
    print("SERVER_PORT="+str(nPort))

    # open the socket for accepting?
    connectionSocket, address = serverSocket.accept()
    # recieve the request code from the client
    incomingReqCode = int(connectionSocket.recv(1024).decode())

    rPort = -1
    # if the request code does not match, close the socket and send an error message
    if(incomingReqCode != reqCode):
        connectionSocket.send(str(rPort).encode())
        serverSocket.close()
        #exit(1)
    # if it does match send back an rPort to make the subsequent requests
    else:
        rPort = findPort()
        connectionSocket.send(str(rPort).encode())



    # UDP

    if(rPort != -1):
        # instantiate a socket for UDP
        serverSocket = socket(AF_INET, SOCK_DGRAM)

        # bind the socket to a host and rPort
        serverSocket.bind(("", rPort))
        print("UDP ready to serve")

        # recieve a message from client, decode it, reverse the string and send it back
        while True:
            message, clientAddress = serverSocket.recvfrom(2048)
            message = message.decode()
            if(message == "EXIT"):
                connectionSocket.close()
                break
            modifiedMessage = message[::-1]
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
            
