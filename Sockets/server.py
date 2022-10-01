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


# TCP

# get the request code from input
reqCode = int(sys.argv[1])

# instantiate a socket for TCP 
tcpServerSocket = socket(AF_INET, SOCK_STREAM)
# bind the socket to 127.0.0.1 and let it pick an open port
tcpServerSocket.bind(("127.0.0.1", 0))
# get the port the socket chose, this is nPort
nPort = tcpServerSocket.getsockname()[1]

# let the socket start listening?
tcpServerSocket.listen(1)

while True:
    # let the client know (in terminal) that the server is listening on nPort
    print("TCP ready to serve")
    print("SERVER_PORT="+str(nPort))

    # open the socket for accepting?
    connectionSocket, address = tcpServerSocket.accept()
    # recieve the request code from the client
    incomingReqCode = int(connectionSocket.recv(1024).decode())

    rPort = -1
    # if the request code does not match, close the socket and send an error message
    if(incomingReqCode != reqCode):
        # send error message
        connectionSocket.send(str(rPort).encode())
        #close the socket
        tcpServerSocket.close()
        break
    # if it does match set up a UDP connection and send back an rPort to make 
    # the subsequent requests
    else:
        # set up a UDP connection
        udpServerSocket = socket(AF_INET, SOCK_DGRAM)
        # bind to an addr and open port
        udpServerSocket.bind(("127.0.0.1", 0))
        # get the rPort
        rPort = udpServerSocket.getsockname()[1]
        # send the rPort to the client
        connectionSocket.send(str(rPort).encode())



    # UDP

    if(rPort != -1):

        while True:
            #recieve the message and address from the client
            message, clientAddress = udpServerSocket.recvfrom(2048)
            # decode the message
            message = message.decode()
            # if the message is exit then close the socket and start over
            if(message == "EXIT"):
                udpServerSocket.close() #?
                connectionSocket.close()
                break
            # reverse the message
            modifiedMessage = message[::-1]
            # send the message back to the client
            udpServerSocket.sendto(modifiedMessage.encode(), clientAddress)
            
