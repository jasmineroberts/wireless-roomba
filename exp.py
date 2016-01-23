import irobot
import time
import string
import socket

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
    r.drive(250,32767)
    while(True):

        fb+=1
        if fb>=5:
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

        bump=[]
        while(len(bump)==0):
            bump=r.sensor_req(7)
        bump=ord(bump[0])
        if bump==1: #right bump turn left
            r.forward(-30,200)
            r.turn(-10,200)
            break
        elif bump==2: #left bump turn right
            r.forward(-30,200)
            r.turn(10,200)
            break
        elif bump==3:  #fron bump turn left
            r.forward(-30,200)
            r.turn(-30,200)
            break
        time.sleep(0.1)
