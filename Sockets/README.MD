# Socket Programming

## Changes to scripts
Changed "python" to "python3" in the client and server scripts.

## Run the programs
To run the programs you can use the server and client scripts.
### Server 
`./server.sh <reqcode>`
### Client
`./client.sh <serverName> <nPort> <reqCode> <message> ... <message>`
### Specifications
`<serverName>` MUST be a string
`<nPort>` MUST be an integer
`<reqCode>` MUST be an integer
`<message>` MUST be a string
*nPort MUST be the same nPort printed out by the server*

## Run on same machine machine
Change the serverName variable in server.py to "127.0.0.1" (line 32), then use this name in the commandline for the client (on the same machine, different terminal)

ex.
1. change severName to "127.0.0.1" in server.py on line 32
2. run server program in a terminal
3. open another terminal on the same machine
4. run the client program with "./client.sh "127.0.0.1" `<nPort>` `<reqCode>` `<messages>`"

## Run on multiple machines
These programs were tested with "ubuntu2004-002" and "ubuntu2004-004" machines.

Change the serverName variable in server.py (line 32) to host machine, then use this name in the commandline for the client (on a different machine)

ex. 
1. login into ubuntu2004-002
2. change serverName to "ubuntu2004-002" on line 32 in server.py
3. run the server program
4. login into ubuntu2004-004 on another terminal
5. run the client program with "./client.sh "ubuntu2004-002" `<nPort>` `<reqCode>` `<messages>`"

## Kill the server
to kill the server, type CTRL+C in the terminal that is running the server