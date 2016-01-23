import pygame
import time
import sys
import socket
import string
import math

#changing IP address
irobotadd=('192.168.0.24',8888)
hostadd=('0.0.0.0',8888)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setblocking(0)
s.bind(hostadd)
PI=3.141592653

curx=400
cury=500
curd=90
x0=400
y0=300

pygame.init()

screen=pygame.display.set_mode([800,600])
screen.fill((255,255,255))
pygame.display.update()

def Event_handler(events):
    for event in events:
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                print 'UP PRESS'
                s.sendto("go 300 32767\n",irobotadd)
            elif event.key==pygame.K_DOWN:
                print 'DOWN PRESS'
                s.sendto("go -300 32767\n",irobotadd)
            elif event.key==pygame.K_LEFT:
                print 'LEFT PRESS'
                s.sendto("go -300 -1\n",irobotadd)
            elif event.key==pygame.K_RIGHT:
                print 'RIGHT PRESS'
                s.sendto("go 300 -1\n",irobotadd)
                
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_UP:
                print 'UP RELEASE'
                s.sendto("go 0 0\n",irobotadd)
            elif event.key==pygame.K_DOWN:
                print 'DOWN RELEASE'
                s.sendto("go 0 0\n",irobotadd)
            elif event.key==pygame.K_LEFT:
                print 'LEFT RELEASE'
                s.sendto("go 0 0\n",irobotadd)
            elif event.key==pygame.K_RIGHT:
                print 'RIGHT RELEASE'
                s.sendto("go 0 0\n",irobotadd)
        elif event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
                


while True:
    Event_handler(pygame.event.get())

    recv=""
    try:
        recv=s.recv(1024)
    except socket.error:
        recv=""

    if recv!="":
        reslist=string.split(recv)
        ddis=string.atoi(reslist[0])*1.0
        ddeg=string.atoi(reslist[1])*1.0
        curd+=ddeg
        tmpx=curx
        tmpy=cury
        curx+=ddis*math.cos((curd/360.0)*2*PI)*0.05
        cury-=ddis*math.sin((curd/360.0)*2*PI)*0.05
        print tmpx
        print tmpy
        print curx
        print cury
        pygame.draw.line(screen,(0,0,0),(tmpx,tmpy),(curx,cury),3)
        pygame.display.update()
    time.sleep(0.1)

