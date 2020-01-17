#!/usr/bin/env python
import socket
import binascii
import subprocess
import sys
import random
from datetime import datetime
from rroll import rroll

# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
#remoteServer    = input("Enter a remote host to scan: ")
#remoteServerIP  = socket.gethostbyname(remoteServer)
#address = socket.gethostbyname('o7jq8f.com')
#address = '10.0.1.1'
address = '159.203.74.94'#'222.186.138.3'#'159.203.74.94'#'194.61.24.7'#'184.105.247.252'
print ("-" * 60)
print ("Please wait, scanning remote host", address)
print ("-" * 60)
while 1:
    # Check what time the scan started
    t1 = datetime.now()
    try:
        count = 0
        #scnPrt=[445,3389,5985]
        scnPrt=[59930,22,111,5900,38764,43800,35722,51848,45780]
        #scnPrt=[34882,5900]
        openPrt =[]
        #for port in range(1,448):  
        for port in scnPrt:  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            lastOct = random.randint(138, 139)
            #source = '10.0.1.' + str(lastOct)
            #sock.bind((source,port))
            server_address = (address, port)
            
            #result = sock.sendto(payload, (server_address))
            result = sock.connect_ex(server_address)
            if result == 0:
                openPrt.append(port)

                #print ("Port {}: 	 Open".format(port))
                #print(r)
            sock.close()
        print(openPrt)
        #for port in openPrt: 
        for roll in rroll: 
                s2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                port2 = random.choice(openPrt)
                server_address = (address, 5900)
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
