#!/usr/bin/env python
# POC: portScanWithRoll.py - 
# If quiet is not your thing
# Send Rick with your pin
# Scan array for open (simple handshake)
# Send all 52 lines of Rick Roll on open socket
# Recieve callfrom Net Admin watching Wireshark asking you to cut it the F-out
# Not an example secure coding.
#Author: scp
#import random #always, always import random...
import socket
import subprocess
import sys
import random
from datetime import datetime
from rroll import rroll

subprocess.call('clear', shell=True)

#address = socket.gethostbyname('example.com')
address = '127.0.0.1'
print ("-" * 60)
print ("Please wait, scanning remote host", address)
print ("-" * 60)
if 1:#while 1:
    # Check what time the scan started
    t1 = datetime.now()
    try:
        count = 0
        scnPrt=[21,22,23,80,5900]# think nc top 20...
        openPrt =[]
        for port in scnPrt: #for port in range(1,448):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (address, port)
            result = sock.connect_ex(server_address)
            if result == 0:
                openPrt.append(port)
            sock.close()
        print(openPrt)
        for port in openPrt: 
           for roll in rroll: 
                   s2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                   port2 = random.choice(openPrt)
                   server_address = (address, port)
                   r = s2.sendto((roll).encode(encoding='utf-8', errors='strict'), (server_address))
                   print("resp:{} roll:{}".format(port2,roll))                
                   s2.close()
                   count=count+1
    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()

    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print ("Couldn't connect to server")
        #sys.exit()

    t2 = datetime.now()
    total =  t2 - t1
    print ("-" * 60)
    print ('Scanning Completed in: ', total)
    print ("-" * 60)
