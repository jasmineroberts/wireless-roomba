import time
import sys,socket
import threading

irobotadd=('192.168.0.24',8888)
hostadd=('0.0.0.0',8888)
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(hostadd)

smutex=threading.Semaphore(1)

def send():
    print "A START"
    while True:
        a=raw_input("Enter:")
        smutex.acquire()
        s.sendto(a,irobotadd)
        smutex.release()

def receive():
    print "B START"
    recv=""
    while True:
        recv=s.recv(1024)
        if recv!="0 0":
            print recv
            recv=""

threada=threading.Thread(None,send)
threadb=threading.Thread(None,receive)
threada.start()
threadb.start()

while(True):
    time.sleep(1)

    
