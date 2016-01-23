import serial
import time

class iRobot:
    def __init__(self,port):
        self.ser=serial.Serial(port,57600,timeout=0)

        self.curx=0
        self.cury=0
        self.curang=0

    def int_to_raw(self,val):
        tmp=val
        return ((tmp>>8)&0xff,tmp&0xff)    

    def w_com(self,data):
        self.ser.write(serial.to_bytes(data))
    
    def w_raw(self,data):
        self.ser.write(data)

    def safe_mode(self):
        self.w_com([128,131])
        time.sleep(0.2)

    def start_script(self,num_byte):
        self.w_com([152])
        self.w_raw(chr(num_byte))

    def end_script(self):
        self.w_com([153])
        
        while(self.ser.read(100)!=''):
            continue

        while(True):
            self.w_com([142])
            self.w_raw(chr(7))
            if self.ser.read(1)!='':
                break
            time.sleep(0.1)
        
        while(self.ser.read(100)!=''):
            continue

    def sensor_req(self,sid):
        while self.ser.read(100)!='':
            continue
        self.w_com([142])
        self.w_raw(chr(sid))
        rlist=[]
        time.sleep(0.1)
        tmp=self.ser.read(1)
        while tmp!='':
            rlist.append(tmp)
            tmp=self.ser.read(1)
        return rlist

    def dump_sensor(self):
        s=""
        for i in range(7,43):
            s+="Sensor Packet"+str(i)+": "
            tmp=self.sensor_req(i)
            for j in range(len(tmp)):
                tmps=bin(ord(tmp[j]))
                s+=tmps[2:]+" "
            s+='\n'
        return s

    def drive(self,vel,r):
        velh,vell=self.int_to_raw(vel)
        rh,rl=self.int_to_raw(r)
        
        self.w_com([137])
        self.w_raw(chr(velh))
        self.w_raw(chr(vell))
        self.w_raw(chr(rh))
        self.w_raw(chr(rl))
   
    def stop(self):
        self.drive(0,0)
 
    def waitfordis(self,dis):
        self.w_com([156])
        dish,disl=self.int_to_raw(dis)
        self.w_raw(chr(dish))
        self.w_raw(chr(disl))

    def waitforang(self,ang):
        self.w_com([157])
        angh,angl=self.int_to_raw(ang)
        self.w_raw(chr(angh))
        self.w_raw(chr(angl))

    def forward(self,dis,vel): #up y+, down y-, left x-, right x+, start at lower left
        self.start_script(13)
        if dis>0:
            self.drive(vel,32767)
        else:
            self.drive(-vel,32767)
        self.waitfordis(dis)
        self.stop()
        self.end_script()
        
        if self.curang==0:
            self.cury+=dis
        elif self.curang==90:
            self.curx+=dis
        elif self.curang==180:
            self.cury-=dis
        elif self.curang==270:
            self.curx-=dis
        time.sleep(0.3)

    def turn(self,deg,vel):     #>0 for clockwise,<0 for counter-clockwise
        if(deg==0):
            return
        self.curang+=deg
        self.start_script(13)
        if deg>0:
            self.drive(vel,-1)
            self.waitforang(-deg)
        
            if self.curang>=360:
                self.curang-=360
        else:
            self.drive(vel,1)
            self.waitforang(-deg)

            if self.curang<0:
                self.curang+=360
        self.stop()
        self.end_script()
        time.sleep(0.3)

    def turn_to(self,deg,vel):
        diff=deg-self.curang
        if diff>180 and diff<=360:
            self.turn(-(360-diff),vel)
        elif diff>0 and diff<=180:
            self.turn(diff,vel)
        elif diff>-180 and diff<=0:
            self.turn(diff,vel)
        else:
            self.turn(diff+360,vel)

    def move_to(self,tarx,tary,vel):
        diffx=tarx-self.curx
        diffy=tary-self.cury

        if diffx>=0 and diffy>=0:
            if diffx>0:
                self.turn_to(90,vel)
                self.forward(diffx,vel)
            if diffy>0:
                self.turn_to(0,vel)
                self.forward(diffy,vel)
        elif diffx<0 and diffy>=0:
            self.turn_to(270,vel)
            self.forward(-diffx,vel)
            if diffy>0:
                self.turn_to(0,vel)
                self.forward(diffy,vel)
        elif diffx<0 and diffy<0:
            self.turn_to(180,vel)
            self.forward(-diffy,vel)
            self.turn_to(270,vel)
            self.forward(-diffx,vel)
        else:
            self.turn_to(180,vel)
            self.forward(-diffy,vel)
            if diffx>0:
                self.turn_to(90,vel)
                self.forward(diffx,vel)

    def return_start(self,vel):
        self.move_to(0,0,vel)
