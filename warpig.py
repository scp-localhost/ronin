#!/usr/bin/env python
# POC: Process pcap-like metadata (much smaller) or Pcap! for Tainted honey/Socket listener(s) Logs
#    Output files contain unique IP, Host, Domain and Script values, any run checks and appends (Lookup is costly)
#    Simple Snort rule templates (some_pig.squeal) was inspiration for name and purpose 
#printf 'test bytes' | nc ['server'] [port]
#printf "GET /nc.1 HTTP/1.1\r\nHost: pote.pw\r\n\r\n" | nc pote.pw 8080'
#printf "pwnly me\r\n\r\n" | nc pote.pw 3389
#curl -v --compressed -H "Range: bytes=0-524288" -H "Connection: close" -A "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)" "$URL"

#https://isc.sans.edu/dashboard.html

#Author: scp
#Todo: Write more DB less text
#    timestamp (and host) as event ID (forign key)
#import random #always, always import random...
import re
import subprocess
import time
import socket
from scapy.all import *
import sys
import whois
from datetime import datetime
import os

cwd = os.getcwd()
top_ports = ['6000','25', '65529','4444', '389', '27017', '21', '23', '8088', '8080', '3389', '5900', '22','80','111']


HOSTS = []
RPORTS = []


domains = []
ips = []
RHOSTS = []
deed = 0

rPortsCnt = []
evilDoers = []
evilDeeds = []
portsCnt = []

class pig:
  def __init__(a_pig, name, doerpath = cwd+ '/evilDoers'+time.strftime('%Y%m%d')+'.txt'\
               , deedpath = cwd+ '/evilDeeds'+time.strftime('%Y%m%d')+'.txt'\
               , pcappath = cwd+ '/evil'+time.strftime('%Y%m%d')+'.pcap'):
    a_pig.cwd = cwd
    a_pig.name = name
    a_pig.ego = '127.0.0.1'
    a_pig.call = []
    a_pig.crap = []
    a_pig.doerpath = doerpath
    a_pig.deedpath = deedpath
    a_pig.pcappath = pcappath

  def poop(this_pig):
    RPORTS = Sort_Tuple(list(rPortsCnt))
    LPORTS = Sort_Tuple(list(portsCnt))
    RHOSTS = Sort_Tuple(list(evilDoers))
    return (LPORTS,RHOSTS,RPORTS)

  def squeal(this_pig,RHOST,RPORT,LHOST,LPORT,t):
    #Snort Rule
    msg = 'msg: "LOCAL.RULES warpig says evil detected";'
    datetime_object = datetime.strptime(t, '%H:%M:%S %m/%d/%y %Z')
    sid = 'sid:' + str(int(datetime_object.timestamp())) + ';'
    snort = 'alert ip '+ RHOST + ' [' +RPORT+ '] -> '+LHOST+ ' '+LPORT+ '('+msg+sid+' rev:666;)' 
    #Shodan
    shodan = 'https://www.shodan.io/host/'+RHOST
    #whois
    whois = 'https://blackhat.directory/ip/'+RHOST
    dnslytics = 'https://dnslytics.com/ip/'+RHOST
    return (snort,shodan,whois)

  def bbq(this_pig):
    print('let\'s eat',this_pig.name)
      
def Sort_Tuple(tup,pos=1):  
    return(sorted(tup, key = lambda x: x[pos]))
def Sort_Tuple_Rev(tup,pos=1):  
    return(sorted(tup, key = lambda x: x[pos], reverse=True))

def formatHosts(hst):#IP's or Hosts
    splt_char = '.'
    tup = hst.split(splt_char) if splt_char in hst else (hst,'')
    return tup
    
def formatDeeds(evilDeed):
    splt_char = ':'
    temp = evilDeed.split(splt_char) 
    res = splt_char.join(temp[:3]), splt_char.join(temp[3:])
    splt_char = ' '
    temp=res[0].split(splt_char)
    res0 = splt_char.join(temp[:3]), splt_char.join(temp[3:])
    LHT = res0[1]
    tstamp = res0[0]
    return (tstamp,LHT)

def formatEvil(evilDoer):
    splt_char = ':'
    temp = evilDoer.split(splt_char) 
    res = splt_char.join(temp[:3]), splt_char.join(temp[3:])
    res2 = re.split(',|:', res[1])
    LPT = res2[0]
    RHT = res2[1]
    RPT = res2[2]
    splt_char = ' '
    temp=res[0].split(splt_char)
    res0 = splt_char.join(temp[:3]), splt_char.join(temp[3:])
    LHT = res0[1]
    tstamp = res0[0]
    
    return (LHT,LPT,RHT,RPT,tstamp),res2,res0[0]

def trackBastards(some_pig,nick,bastard):
    f = some_pig.cwd+'/'+nick+'.txt'
    bastards = []
    try:
        bastards = loadBastards(some_pig,nick)
    except:
        bastards = []
    if bastard not in bastards:                    
        with open(f , 'a') as myfile:
           evil = bastard +'\n'
           myfile.write(evil)

def loadBastards(some_pig,nick):
    f = some_pig.cwd+'/'+nick+'.txt'
    bastards = []
    try:
        with open(f) as fp:
           line = fp.readline()
           while line:
               bastards.append(line.strip())
               line = fp.readline()
    except:
        bastards = []
    return bastards

def printBastards(some_pig,nick):
        bastards = loadBastards(some_pig,nick)
        currentBastards = []
        for bastard in bastards:
            currentBastards.append(formatHosts(bastard))
        temp = Sort_Tuple(currentBastards,-2)
        for bastard in temp:
            bastards.append(('.').join(bastard))
            print(('.').join(bastard))

def readPcap(some_pig):
    pcrap = []
    pcap = rdpcap(some_pig.pcappath)  
    for p in pcap:
        if p.haslayer(TCP):
            if ((p[IP].dst == some_pig.ego or p[IP].src == some_pig.ego ) and (str(p[TCP].dport) in top_ports)):
                RHOST = p[IP].src
                RPORT = p[TCP].sport
                LHOST = some_pig.ego
                LPORT = p[TCP].dport
                timestamp = int(p.time)
                pcrap.append((RHOST,RPORT,LHOST,LPORT,timestamp))
    some_pig.crap = pcrap

def readEvil(some_pig):
    pcrap=[]
    with open(some_pig.doerpath) as fp:
       line = fp.readline()
       while line:
           c=formatEvil(line.strip())
           RHOST = c[0][2]
           RPORT = c[0][3]
           LHOST = c[0][0]
           LPORT = c[0][1]
           timestamp = c[0][4]
           pcrap.append((RHOST,RPORT,LHOST,LPORT,timestamp))
           line = fp.readline()
    some_pig.crap = pcrap

def readDeeds(some_pig):
    pcrap=[]
    with open(some_pig.deedpath) as fp:
       line = fp.readline()
       while line:
           t=formatDeeds(line.strip())
           line = fp.readline()
           s=line.strip()
           pcrap.append((t,s))
           deed = 1
           line = fp.readline()
    some_pig.call = pcrap           

def tallys(some_pig):
    for line in some_pig.call:
        #print(line[0])
        found = 0
        for idx, script in enumerate(evilDeeds):
           if (script[0] == line[1]):
               evilDeeds[idx] = (line[1],script[1] + 1)
               found = 1
        if (found == 0) and (line[1][0] == 'b'):
            evilDeeds.append((line[1] ,1))
            trackBastards(some_pig,'BastardScripts',line[1])
    for pkt in some_pig.crap:
        found = 0
        for idx, doer in enumerate(evilDoers):
           if (doer[0] == pkt[0]):
               evilDoers[idx] = (pkt[0],doer[1] + 1)
               found = 1
        if found == 0:
            evilDoers.append((pkt[0],1))
            trackBastards(some_pig,'BastardIPs',pkt[0])
        dst = str(pkt[3])
        found = 0
        for idx, prt in enumerate(portsCnt):
           if prt[0] == dst:
               portsCnt[idx] = (dst,prt[1] + 1)
               found = 1
        if found == 0:portsCnt.append((dst,1))
        dst = str(pkt[1])
        found = 0
        for idx, prt in enumerate(rPortsCnt):
           if prt[0] == dst:
               rPortsCnt[idx] = (dst,prt[1] + 1)
               found = 1
        if found == 0:rPortsCnt.append((dst,1))
    if 'you wish' and False:
        for idx, doer in enumerate(evilDoers):
            try:
                hst = socket.gethostbyaddr(doer[0])
                if hst not in HOSTS:HOSTS.append(hst)
                trackBastards(some_pig,'BastardHosts',hst[0])
                domain = whois.query(hst[0])
                if domain.name not in domains:domains.append(domain.name)
                trackBastards(some_pig,'BastardDomains',domain.name)
            except:
                if doer[0] not in ips:ips.append(doer[0])

def dbLand(some_pig,nick='Scripts'):
    #https://www.sqlite.org/inmemorydb.html
    import sqlite3
    conn = sqlite3.connect('/home/papa/Bastards.db')
    #You can also supply the special name :memory: to create a database in RAM.
    #scripts, ips, hosts, domains, cap?
    c = conn.cursor()
    c.execute('drop table if exists ' + nick)
    c.execute('create table if not exists ' + nick + ' (last_seen INT NOT NULL DEFAULT 0,' + nick + ' TEXT, UNIQUE(' + nick + ') ON CONFLICT REPLACE )''')
    #c.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name=?',[some_table])
    #print(c.fetchone()[0]==1)
    for i in sorted(list(loadBastards(some_pig,'Bastard' + nick))):
        #print(i)
        c.execute('INSERT INTO ' + nick + ' VALUES (0,?)', [i])
    for i in c.execute('SELECT * FROM ' + nick + ' ORDER BY ' + nick):
            print(i)
    conn.commit()
    conn.close()

def doStuff(some_pig):
    if deed:
        some_pig.squeal()
    else:
        if HOSTS != []: print(HOSTS)
        if ips != []: print(ips)
        if domains != []: print(domains)
        printBastards(some_pig,'BastardHosts')
        for i in sorted(list(loadBastards(some_pig,'BastardScripts'))):
            print(i)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        evilDoerpath = sys.argv[1]    
        if len(sys.argv) > 2:
            evilDeedpath = sys.argv[2]    
        else : evilDeedpath = '/home/papa/evilDeeds'+time.strftime('%Y%m%d')+'.txt'
        mainPig = pig('wilbur',evilDoerpath,evilDeedpath)

        readDeeds(mainPig)
        print(mainPig.call)
        readEvil(mainPig)
        tallys(mainPig)
        doStuff(mainPig) 
        
    elif 1 : 
        mainPig = pig('babe')
        mainPig.deedpath = '/home/papa/evilDeeds20191223.txt'
        mainPig.pcappath = '/soil/home/papa/Yandex.Disk/pcap/warpigFodder20191212.pcap'
        readDeeds(mainPig)

        readPcap(mainPig)
        tallys(mainPig)
        doStuff(mainPig)
        dbLand(mainPig,'Scripts')
        dbLand(mainPig,'Hosts')
        dbLand(mainPig,'Domains')
        dbLand(mainPig,'IPs')
        mainPig.bbq()
    else:
        dbLand()
