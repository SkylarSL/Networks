from socket import *
import sys
from packet import Packet

def getUDPConnection(addr, port):
    # instantiate a UDP connection
    udpServerSocket = socket(AF_INET, SOCK_DGRAM)
    # bind to an addr and open port
    udpServerSocket.bind((addr, port))
    return udpServerSocket

# check for number of arguments
if(len(sys.argv) < 5):
    print("not enough arguments")
    exit(1)

# accept commandline arguments and assign them
emulatoraddr = sys.argv[1]
emulatorport = int(sys.argv[2])
receiverport = int(sys.argv[3])
filename = sys.argv[4]

def seqnummod(x):
    return x % 32

# set up a UDP connection
udpServerSocket = getUDPConnection("", receiverport)

file = open(filename, "w")
file.write("")
file.close()
file = open(filename, "a")
log = open("arrival.log", "w")
log.write("")
log = open("arrival.log", "a")
buffer = []
expectedseqnum = 0
recievedseqnum = 0
firsttime = 0
while True:
    #recieve the message and address from the client
    message, clientAddress = udpServerSocket.recvfrom(1024)
    # decode the message
    packet = Packet(message)
    log.write(str(packet.seqnum) + "\n")

    seqnum = packet.seqnum
    type = packet.typ
    message = packet.data
    
    if seqnum == seqnummod(expectedseqnum):
        if type == 2:
            # send the message back to the client
            packet = Packet(2, 0, 0, "")
            udpServerSocket.sendto(Packet.encode(packet), (emulatoraddr, emulatorport))
            message = packet.data
            # write to a file
            break
        else:
            file.write(message)
            expectedseqnum += 1
            inbuffer = True
            while inbuffer:
                inbuffer = False
                for packet in buffer:
                    # if expected packet is in the buffer
                    if packet.seqnum == expectedseqnum:
                        # remove packet from buffer
                        buffer.remove(packet)
                        # write data to output file
                        file.write(message)

                        # check next seqnum
                        expectedseqnum += 1
                        # packet is in the buffer
                        inbuffer = True
            # if the packet is not in the buffer
            if not inbuffer:
                recievedseqnum = expectedseqnum - 1 
                packet = Packet(0, seqnummod(recievedseqnum), 0, "")
                udpServerSocket.sendto(Packet.encode(packet), (emulatoraddr, emulatorport))
    else:
        if packet.seqnum < expectedseqnum + 10 and packet not in buffer:
            packet = Packet(0, seqnum, 0, "")
            buffer.append(packet)
            recievedseqnum = seqnum
        packet = Packet(0, seqnummod(expectedseqnum), 0, "")
        udpServerSocket.sendto(Packet.encode(packet), (emulatoraddr, emulatorport))

file.close()
log.close()

