#BeagleBoneBlack Main

import irobot
import time
import sys
import socket
import string

r=irobot.iRobot('/dev/ttyO1')
r.safe_mode()

address=('0.0.0.0',8888)
hostadd=('192.168.0.3',8888)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.settimeout(0)
s.bind(address)

def negbin(high,low):
    highd=ord(high)
    lowd=ord(low)
    if highd & (1<<7):
        highd=highd - (1<<7)
        return ((highd<<8)+lowd)-(1<<15)
    return (highd<<8)+lowd
        

fb=0
while(True):
    fb+=1
    time.sleep(0.05)
    data=""
    cmdlist=[]

    if fb>=20:
        fb=0
        tmp=[]
        dres=-1
        ares=-1
        tmp=r.sensor_req(19)
        if len(tmp)>0:
            dres=negbin(tmp[0],tmp[1])
        #print tmp
        #print ord(tmp[0])<<8+ord(tmp[1])
        tmp=[]
        tmp=r.sensor_req(20)
        if len(tmp)>0:
            ares=negbin(tmp[0],tmp[1])
        print ares
        if ares!=0 or dres!=0:
            udpstr=str(dres)+' '+str(ares)
            #print udpstr
            s.sendto(udpstr,hostadd)

    try:
        data=s.recv(100)
        print 'data:'
        print data
    except socket.error,e:
        data=""

    if data!="":
        cmdlist=string.split(data)
        print cmdlist[0]
        if cmdlist[0]=='drive':
            dis=string.atoi(cmdlist[1])
            vel=string.atoi(cmdlist[2])
            r.forward(dis,vel)
        elif cmdlist[0]=='turn':
            deg=string.atoi(cmdlist[1])
            vel=string.atoi(cmdlist[2])
            r.turn(deg,vel)
        elif cmdlist[0]=='dump':
            tmps=r.dump_sensor()
            print tmps
            s.sendto(tmps,hostadd)
            print 'Dump ok!\n'
        elif cmdlist[0]=='goto':
            tarx=string.atoi(cmdlist[1])
            tary=string.atoi(cmdlist[2])
            vel=string.atoi(cmdlist[3])
            r.move_to(tarx,tary,vel)
        elif cmdlist[0]=='return':
            vel=string.atoi(cmdlist[1])
            r.return_start(vel)
        elif cmdlist[0]=='go':
            r.drive(string.atoi(cmdlist[1]),string.atoi(cmdlist[2]))
        #s.sendto("Success!\n",hostadd)
