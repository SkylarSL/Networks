from packet import Packet
import sys
from socket import *
from threading import Thread, Timer, Lock, Condition

#global variables
i = 0 # variables for window size
windowsize = 1 # variables for window size
acklock = Lock() 
ackcond = Condition(acklock) # conditional lock to sync sender and receiver
udpClientSocket = socket(AF_INET, SOCK_DGRAM) 
expectedseqnum = 0
numpackets = 0
timestamp = 0

# log files
seqnumlog = open("seqnum.log", "w")
seqnumlog.write("")
acklog = open("ack.log", "w")
acklog.write("")
Nlog = open("N.log", "w")
Nlog.write("")
seqnumlog = open("seqnum.log", "a")
acklog = open("ack.log", "a")
Nlog = open("N.log", "a")

# check for number of arguments
if len(sys.argv) < 6:
    print("not enough arguments")
    exit(1)
# accept commandline arguments and assign them
emulatoraddr = sys.argv[1]
emulatorport = int(sys.argv[2])
senderport = int(sys.argv[3])
timeout = int(sys.argv[4])
filename = sys.argv[5]

# timer functions
def timerupfunc():
    global windowsize, i, timeout, Nlog, timestamp
    windowsize = 1
    Nlog.write("t=" + str(timestamp) + " " + str(windowsize) + "\n")
    if i < len(window):
        udpClientSocket.sendto(Packet.encode(window[i]), (emulatoraddr, emulatorport))
        seqnumlog.write("t=" + str(timestamp) + " " + str(window[i].seqnum) + "\n")
    timestamp += 1
    newtimer()
    with ackcond:
        ackcond.notify()
    return 0
# initialize timer
timer = Timer(timeout/1000, timerupfunc)
# create and start a new timer
def newtimer():
    global timer, timerup, timeout
    timer.cancel()
    timer = Timer(timeout/1000, timerupfunc)
    timer.start()
    return 0
# stop the timer
def stoptimer():
    timer.cancel()

# simple func to calculate x mod32
def seqnummod(x):
    return x % 32

# read the file contents and break into 500 character packets
file = open(filename, "r")
data = file.read()
tmp = ""
window = []
sequencenum = 0
# break up the data into packets of size 500 characters
for p in range(0, len(data)):
    if p != 0 and p % 500 == 0:
        newpacket = Packet(1, seqnummod(sequencenum), len(tmp), tmp)
        window.append(newpacket)
        tmp = ""
        sequencenum += 1
    tmp+=data[p]
newpacket = Packet(1, seqnummod(sequencenum), len(tmp), tmp)
window.append(newpacket)
newpacket = Packet(2, seqnummod(sequencenum+1), 0, "")
window.append(newpacket)
sentpackets = []
numpackets = sequencenum + 1

# separate window to keep track of ACKed packets
ackwindow = [x.typ for x in window]

Nlog.write("t=" + str(timestamp) + " " + str(windowsize) + "\n")
timestamp += 1

# send thread
def send():

    # global variables
    global window, ackwindow, windowsize, ackcond, i, sentpackets, udpClientSocket, seqnumlog, Nlog, timestamp

    with ackcond:
        while True:     
            fullwindow = True
            # initialization, first send
            if i == 0:
                windowsize = 1
                udpClientSocket.sendto(Packet.encode(window[i]), (emulatoraddr, emulatorport))
                sentpackets.append(window[i])
                seqnumlog.write("t=" + str(timestamp) + " " + str(window[i].seqnum) + "\n")
                timestamp += 1
                i += 1
                newtimer()
                ackcond.notify()

            # check for a full window
            while fullwindow:
                ackcond.wait()
                for packet in range(i, i+windowsize):
                    if packet < len(window):
                        if ackwindow[packet] != 0 and window[packet] not in sentpackets:
                            fullwindow = False
                            break
            
            # close application if last packet (EOT) is acknowledged
            if i >= len(ackwindow)-1 and ackwindow[i-1] == 0:
                exit()

            # send packets
            if (not fullwindow) and i != 0:
                udpClientSocket.sendto(Packet.encode(window[i]), (emulatoraddr, emulatorport))
                seqnumlog.write("t=" + str(timestamp) + " " + str(window[i].seqnum) + "\n")
                timestamp += 1
                sentpackets.append(window[i])
                i += 1
                ackcond.notify()

# receive thread
def receive():
    global ackwindow, window, windowsize, expectedseqnum, i, ackcond, udpClientSocket, acklog, Nlog, seqnumlog, timestamp

    # bind to an addr and open port
    udpClientSocket.bind(("", senderport))
    
    # pair to track duplicate acks
    dupack = [-1, 0]
    with ackcond:
        while True:
            # only wait if there are still packets to be sent
            if len(sentpackets) <= numpackets:
                ackcond.wait()

            # recieve the packet
            message, serverAddress = udpClientSocket.recvfrom(1024)
            packet = Packet(message)
            seqnum = seqnummod(packet.seqnum)
            type = packet.typ

            # cumulative ACKs
            for p in range(0, i):
                ackwindow[p] = 0
                
            # ACK for EOT packet
            if type == 2:
                # check if all packets have been sent
                if len(sentpackets) >= numpackets:
                    acklog.write("t=" + str(timestamp) + " " + "EOT" + "\n")
                    stoptimer()
                    udpClientSocket.close()
                    seqnumlog.close()
                    Nlog.close()
                    acklog.close()
                    break
            else:
                acklog.write("t=" + str(timestamp) + " " + str(packet.seqnum) + "\n")
            timestamp += 1

            # if the packet is a duplicate
            if seqnum == dupack[0]:
                dupack[1] += 1

            # if the packet is not a duplicate
            else:
                # if there are transmitted-but-yet-to-be-acknowldged packets
                for packet in range(i, i+windowsize):
                    if packet < len(window):
                        if ackwindow[packet] != 0:
                            newtimer()
                            break
                # if there are new ACKs
                if windowsize < 10:
                    windowsize += 1
                    Nlog.write("t=" + str(timestamp) + " " + str(windowsize) + "\n")
                if len(sentpackets) <= numpackets:
                    ackcond.notify()
                dupack = [seqnum, 0]

            # if there are 3 duplicate ACKs
            if dupack[1] >= 3:
                windowsize = 1
                Nlog.write("t=" + str(timestamp) + " " + str(windowsize) + "\n")
                udpClientSocket.sendto(Packet.encode(window[dupack[0]]), (emulatoraddr, emulatorport))
                seqnumlog.write("t=" + str(timestamp) + " " + str(window[i].seqnum) + "\n")
                timestamp += 1
                newtimer()
        
        # notify last packet to close application
        ackcond.notifyAll()
        exit()

# threads
senderfunc = Thread(target=send, name="send")
receiverfunc = Thread(target=receive, name="receive")

receiverfunc.start()
senderfunc.start()

exit()