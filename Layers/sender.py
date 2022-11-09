from packet import Packet
import sys
from socket import *
# experiments
import time
from threading import Thread, Timer, Lock, Condition
import random

#global variables
windowsize = 1 # window size
timerlock = Lock()
acklock = Lock()
ackcond = Condition(acklock)
windowlock = Lock()
windowcond = Condition(windowlock)
timerup = False

# timer functions
def timerupfunc():
    global timerup
    print("timer ran out")
    timerlock.acquire()
    timerup = True
    timerlock.release()
    return 0
timer = Timer(3, timerupfunc)
def newtimer():
    global timer, timerup
    print("resetting timer")
    timerlock.acquire()
    timerup = False
    timerlock.release()
    timer.cancel()
    timer = Timer(3, timerupfunc)
    timer.start()
    return 0
def stoptimer():
    timer.cancel()

def seqnummod(x):
    return x % 32

# check for number of arguments
if len(sys.argv) < 6:
    print("not enough arguments")
    exit(1)
# accept commandline arguments and assign them
emulatoraddr = sys.argv[1]
emulatorport = int(sys.argv[2])
senderport = int(sys.argv[3])
timeout = sys.argv[4]
filename = sys.argv[5]

# read the file contents and break into 500 character packets
file = open(filename, "r")
data = file.read()
tmp = ""
window = []
sequencenum = 0
# break up the data into packets of size 500 characters
for i in range(0, len(data)):
    if i != 0 and i % 500 == 0:
        newpacket = Packet(1, seqnummod(sequencenum), len(tmp), tmp)
        window.append(newpacket)
        tmp = ""
        sequencenum += 1
    tmp+=data[i]
newpacket = Packet(1, seqnummod(sequencenum), len(tmp), tmp)
window.append(newpacket)
newpacket = Packet(2, seqnummod(sequencenum+1), 0, "")
window.append(newpacket)

# window
i = 0
expectedseqnum = 0
def send():
    udpClientSocket = socket(AF_INET, SOCK_DGRAM)
    print("starting sender thread...")
    global window
    global windowsize
    global ackcond
    global windowcond
    global i

    # check if window is full
    while(True):
        time.sleep(random.random()*2) # experiment
        
        # check for unacknowledged packets
        fullwindow = True
        with ackcond:
            if i == i+windowsize-1:
                fullwindow = False
            else:
                for packet in range(i, i+windowsize):
                    if packet < len(window):
                        print(window[packet].typ)
                        if window[packet].typ == 0:
                            print("ACK")
                            fullwindow = False
                            break
            # send packets
            if not fullwindow:
                print("sending")
                udpClientSocket.sendto(Packet.encode(window[i]), (emulatoraddr, emulatorport))
                i += 1
            ackcond.notify()
            # i += 1
            newtimer()

        # break

def receive():
    udpClientSocket = socket(AF_INET, SOCK_DGRAM)
    # bind to an addr and open port
    udpClientSocket.bind((emulatoraddr, senderport))
    print("starting receiver thread...")
    global window
    global windowsize
    global expectedseqnum
    global i
    global ackcond
    global windowcond

    dupack = [-1, -1]
    while True:
        time.sleep(1) # experiment
        print("receiving")

        # timer ran out, timeout occured
        if timerup:
            print("FUCK")
            windowsize = 1
            udpClientSocket.sendto(Packet.encode(window[i]), (emulatoraddr, emulatorport))
            newtimer()

        # recieve the packet
        message, serverAddress = udpClientSocket.recvfrom(1024)
        packet = Packet(message)
        print(packet)

        seqnum = seqnummod(packet.seqnum)
        type = packet.typ

        with ackcond:
            ackcond.wait()
            for packet in range(0, seqnum+1):
                window[packet].typ = 0

            # if the packet is a duplicate
            if seqnum == dupack[0]:
                dupack[1] += 1
            # if the packet is not a duplicate
            else:
                # if there are transmitted-but-yet-to-be-acknowldged packets
                for packet in range(i, i-windowsize):
                    if packet < len(window):
                        if window[packet].seqnum != 0:
                            newtimer()
                            break
                # if there are new ACKs
                if windowsize < 10:
                    windowsize += 1
                dupack = [seqnum, 0]

            # if there are 3 duplicate ACKs
            if dupack[1] == 3 and seqnum == expectedseqnum:
                windowsize = 1
                newtimer()
                udpClientSocket.sendto(Packet.encode(window[i]), (emulatoraddr, emulatorport))


senderfunc = Thread(target=send, name="send")
receiverfunc = Thread(target=receive, name="receive")

senderfunc.start()
receiverfunc.start()


