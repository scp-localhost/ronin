#!/usr/bin/env python
# socketZardoz.py - 
# Send zardoz to IP and port
# Useful if you just aren't getting the attention an open socket deserves
# ***This is SOOO the packets you want forensics to reconstruct!
# Not an example secure coding.
#Author: scp
#import random #always, always import random...
import sys, socket
import zarBits
server = (('127.0.0.1', 6666))#When I think about you...
if len(sys.argv) > 2: server = ((sys.argv[1] , int(sys.argv[2])))
with open('/home/papa/zardoz.jpg', 'rb') as f:b=f.read()
b = zarBits.zardoz()#zardoz jpg as bits
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server)
s.send(b)
s.close()
