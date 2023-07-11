# Reliable Data Transfer

## Parameters

#### Servers
This was tested on the following servers with respective applications:
1. ubuntu2004-008, network emulator
2. ubuntu2004-002, sender
3. ubuntu2004-004, receiver

#### Port issues 
If the ports do not work you can run the command:
`comm -23 <(seq 1024 65535 | sort) <(ss -tan | awk '{print $4}' | cut -d':' -f2 | grep "[0-9]\{1,5\}" | sort -u) | shuf | head -n 4`
this will output 4 ports that can be used. Just replace the appropriate ports in the script files.

#### Reference
For ease of reference here is how the paramters should match up all together (with example ports):
1. emulator.sh: `<port1>` "ubuntu2004-004" `<port4>` `<port3>` "ubuntu2004-002" `<port2>` 1 0.2 0
2. sscript.sh: "ubuntu2008-008" `<port3>` `<port4>` input.txt
3. rscript.sh: "ubuntu2008-008" `<port1>` `<port2>` 50 output.txt

#### Files
The file to be sent is the input.txt file. You can replace the text with anything you want. Right now it is just a ton of Lorem Ipsum.

## Run

The folder should contain script files that can be executed to run the programs:
1. emulator.sh, run network emulator
2. sscript.sh, run sender
3. rscript.sh, run receiver

#### Steps
1. Open 3 terminals ssh into ubuntu2004-008, ubuntu2004-004, ubuntu2004-002 (each on a separate terminal)
2. For each terminal cd into the assignment folder with the scripts
3. In ubuntu2004-008, run `./emulator.sh`
4. In ubuntu2004-004, run `./rscript.sh`
5. in ubuntu2004-002, run `./sscript.sh`

After the above, the output files and log files should be apprpriately filled.
