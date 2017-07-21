#coding:utf-8
'''
树莓派WiFi无线视频小车机器人驱动源码
作者：liuviking
版权所有：小R科技（深圳市小二极客科技有限公司）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
'''

from socket import *
from time import ctime
import binascii
import RPi.GPIO as GPIO
import time
import threading

print '....WIFIROBOTS START!!!...'

SPEED=35
FREQUENCY=50


#######################################
#############信号引脚定义##############
#######################################
GPIO.setmode(GPIO.BCM)



########LED口定义#################
LED0 = 10
LED1 = 99
LED2 = 25


########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

########舵机接口定义#################
SER1 = 11	#舵机1
SER2 = 8	#舵机2
SER3 = 7	#舵机3
SER4 = 5	#舵机4
SER7 = 6	#垂直舵机接口7号舵机
SER8 = 12	#水平舵机接口8号舵机

########超声波接口定义#################
ECHO = 4	#超声波接收脚位  
TRIG = 17	#超声波发射脚位

########红外传感器接口定义#################
IR_R = 18	#小车右侧巡线红外
IR_L = 27	#小车左侧巡线红外
IR_M = 22	#小车中间避障红外
IRF_R = 23	#小车跟随右侧红外
IRF_L = 24	#小车跟随左侧红外
global Cruising_Flag
Cruising_Flag = 0	#//当前循环模式
global Pre_Cruising_Flag
Pre_Cruising_Flag = 0 	#//预循环模式
Left_Speed_Hold = 255	#//定义左侧速度变量
Right_Speed_Hold = 255	#//定义右侧速度变量
buffer = ['00','00','00','00','00','00']

#######################################
#########管脚类型设置及初始化##########
#######################################
GPIO.setwarnings(False)

#########led初始化为000##########
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
#GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)

#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,FREQUENCY) 
ENA_pwm.start(SPEED) 
ENA_pwm.ChangeDutyCycle(SPEED)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,FREQUENCY)
ENB_pwm.start(SPEED) 
ENB_pwm.ChangeDutyCycle(SPEED)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)



#########红外初始化为输入，并内部拉高#########
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)


#GPIO.output(ENA,True)
#GPIO.output(ENB,True)

##########超声波模块管脚类型设置#########
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW)#超声波模块发射端管脚设置trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP)#超声波模块接收端管脚设置echo

##########舵机管脚类型设置#########

GPIO.setup(SER1,GPIO.OUT)#1号舵机
GPIO.setup(SER2,GPIO.OUT)#2号舵机
GPIO.setup(SER3,GPIO.OUT)#3号舵机
GPIO.setup(SER4,GPIO.OUT)#4号舵机
GPIO.setup(SER7,GPIO.OUT)#水平舵机接口7号舵机
GPIO.setup(SER8,GPIO.OUT)#垂直舵机接口8号舵机
Servo7=GPIO.PWM(SER7,50) #50HZ  
Servo7.start(0)  
Servo8=GPIO.PWM(SER8,50) #50HZ  
Servo8.start(0)  


####################################################
##函数名称 Open_Light()
##函数功能 开大灯LED0
##入口参数 ：无
##出口参数 ：无
####################################################
def	Open_Light():#开大灯LED0
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	time.sleep(1)

####################################################
##函数名称 Close_Light()
##函数功能 关大灯
##入口参数 ：无
##出口参数 ：无
####################################################
def	Close_Light():#关大灯
	GPIO.output(LED0,True)#大灯正极接5V  负极接IO口
	time.sleep(1)
	
####################################################
##函数名称 init_light()
##函数功能 流水灯
##入口参数 ：无
##出口参数 ：无
####################################################
def	init_light():#流水灯
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	time.sleep(0.5)
	GPIO.output(LED0,True)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	time.sleep(0.5)
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	time.sleep(0.5)
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口
	time.sleep(0.5)
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	time.sleep(0.5)
	GPIO.output(LED0,True)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口
##########机器人方向控制###########################
def Motor_Forward():
	print 'motor forward'
	ENA_pwm.ChangeDutyCycle(SPEED)
	ENB_pwm.ChangeDutyCycle(SPEED)
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	
def Motor_Backward():
	print 'motor_backward'
	ENA_pwm.ChangeDutyCycle(SPEED)
        ENB_pwm.ChangeDutyCycle(SPEED)
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	
def Motor_TurnLeft():
	print 'motor_turnleft'
	ENA_pwm.ChangeDutyCycle(SPEED)
        ENB_pwm.ChangeDutyCycle(SPEED)
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口
def Motor_TurnRight():
	print 'motor_turnright'
	ENA_pwm.ChangeDutyCycle(SPEED)
        ENB_pwm.ChangeDutyCycle(SPEED)
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口

def ENA_Speed(EA_num):
	speed=hex(eval('0x'+EA_num))
	speed=int(speed,16)
	ENA_pwm.ChangeDutyCycle(speed)

def ENB_Speed(EB_num):
	speed=hex(eval('0x'+EB_num))
	speed=int(speed,16)
	ENB_pwm.ChangeDutyCycle(speed)	
#舵机角度驱动函数    
def SetServo7Angle(angle_from_protocol):
	angle=hex(eval('0x'+angle_from_protocol))
	angle=int(angle,16)
	Servo7.ChangeDutyCycle(2.5 + 10 * angle / 180) #设置水平舵机转动角度 
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,False)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口
	time.sleep(0.01)
	GPIO.output(LED0,True)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口
def SetServo8Angle(angle_from_protocol):
	angle=hex(eval('0x'+angle_from_protocol))
	angle=int(angle,16)
	Servo8.ChangeDutyCycle(2.5 + 10 * angle / 180) #设置垂直舵机转动角度
	GPIO.output(LED0,False)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,False)#大灯正极接5V  负极接IO口
	time.sleep(0.01)
	GPIO.output(LED0,True)#大灯正极接5V  负极接IO口
	#GPIO.output(LED1,True)#大灯正极接5V  负极接IO口
	GPIO.output(LED2,True)#大灯正极接5V  负极接IO口


####################################################
##函数名称 ：Avoiding()
##函数功能 ：红外避障函数
##入口参数 ：无
##出口参数 ：无
####################################################
def	Avoiding(): #红外避障函数
	if GPIO.input(IR_M) == False:
		Motor_Stop()
		return
	else:
		Motor_Forward()
		return

####################################################
##函数名称 FollowLine()
##函数功能 巡黑线模式
##入口参数 ：无
##出口参数 ：无
####################################################
def FollowLine():
	if (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == False): #黑线为高，地面为低
		Motor_Forward()
		time.sleep(0.05)
		Motor_Stop()
		time.sleep(0.05)
		return
	elif (GPIO.input(IR_L) == False)&(GPIO.input(IR_R) == True):
		Motor_TurnRight()
		time.sleep(0.1)
		Motor_Stop()
		time.sleep(0.05)
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == False):
		Motor_TurnLeft()
		time.sleep(0.1)
		Motor_Stop()
		time.sleep(0.05)
		return
	elif (GPIO.input(IR_L) == True)&(GPIO.input(IR_R) == True): #两侧都碰到黑线
		Motor_Stop()
		return

####################################################
##函数名称 ：Get_Distence()
##函数功能 超声波测距，返回距离（单位是米）
##入口参数 ：无
##出口参数 ：无
####################################################
def	Get_Distence():
	time.sleep(0.1)
	GPIO.output(TRIG,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TRIG,GPIO.LOW)
	while not GPIO.input(ECHO):
				pass
	t1 = time.time()
	while GPIO.input(ECHO):
				pass
	t2 = time.time()
	time.sleep(0.1)
	return (t2-t1)*340/2

####################################################
##函数名称 Avoid_wave()
##函数功能 超声波避障函数
##入口参数 ：无
##出口参数 ：无
####################################################
def	Avoid_wave():
	dis = Get_Distence()
	if dis<0.15:
		Motor_Stop()
	else:
		Motor_Forward()

####################################################
##函数名称 Send_Distance()
##函数功能 ：超声波距离PC端显示
##入口参数 ：无
##出口参数 ：无
####################################################
def	Send_Distance():
	dis_send = Get_Distence()
	if dis < 4:
		print 'Distance: %0.3f m' %dis_send
		time.sleep(1)


def	Cruising_Mod(func):
	print 'into Cruising_Mod-01'
	global Pre_Cruising_Flag
	print 'Pre_Cruising_Flag %d '%Pre_Cruising_Flag
	
	global Cruising_Flag
	print 'Cruising_Flag %d '%Cruising_Flag
	while True:
		if (Pre_Cruising_Flag != Cruising_Flag):			
			if (Pre_Cruising_Flag != 0):
				Motor_Stop()
			Pre_Cruising_Flag = Cruising_Flag
			print 'Pre_Cruising_Flag = Cruising_Flag == 0'
		if(Cruising_Flag == 2):	#进入红外巡线循迹模式
			FollowLine()
		elif (Cruising_Flag == 3):	#进入红外避障模式
			Avoiding()
		elif (Cruising_Flag == 4):	#进入超声波壁障模式
			Avoid_wave()
		else:
			time.sleep(0.001)
		time.sleep(0.001)







    
#通信协议解码   
def Communication_Decode():
	global Pre_Cruising_Flag
	global Cruising_Flag
	print 'Communication_decoding...'
	if buffer[0]=='00':
		if buffer[1]=='01':			#前进
			Motor_Forward()
		elif buffer[1]=='02':			#后退
			Motor_Backward()
		elif buffer[1]=='03':			#左转
			Motor_TurnLeft()
		elif buffer[1]=='04':			#右转
			Motor_TurnRight()
		elif buffer[1]=='00':			#停止
			Motor_Stop() 
		else:
			Motor_Stop()
	elif buffer[0]=='01':
		if buffer[1]=='07':#7号舵机驱动
			SetServo7Angle(buffer[2])
		elif buffer[1]=='08':#8号舵机驱动
			SetServo8Angle(buffer[2])
	elif buffer[0]=='02':
		if buffer[1]=='01':#7号舵机驱动
			ENA_Speed(buffer[2])
			print 'ENA_Speed 改变啦%d '
		elif buffer[1]=='02':#8号舵机驱动
			ENB_Speed(buffer[2])
			print 'ENB 改变啦%d '
	elif buffer[0]=='13':
		if buffer[1]=='02':
			Cruising_Flag = 2#进入红外巡线循迹模式
			print 'Cruising_Flag改变啦 %d '%Cruising_Flag
		elif buffer[1]=='03':#进入红外避障模式
			Cruising_Flag = 3
			print 'Cruising_Flag改变啦 %d '%Cruising_Flag
		elif buffer[1]=='04':#进入超声波壁障模式
			Cruising_Flag = 4
			print 'Cruising_Flag改变啦 %d '%Cruising_Flag
		elif buffer[1]=='00':
			Cruising_Flag = 0
			print 'Cruising_Flag 改变啦%d '%Cruising_Flag
		#else:
			#Cruising_Flag = 0
	elif buffer[0]=='05':
		if buffer[1]=='00':
			Open_Light()
		elif buffer[1]=='01':
			Close_Light()
		else:
			print '...'
	else:
		print '...'
            



init_light()

#定义TCP服务器相关变量
HOST=''
PORT=2001
BUFSIZ=1
ADDR=(HOST,PORT)
rec_flag=0
i=0
buffer=[]
#启动TCP服务器，监听2001端口
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(1)

threads = []
t1 = threading.Thread(target=Cruising_Mod,args=(u'监听',))
threads.append(t1)

for t in threads:
		t.setDaemon(True)
		t.start()

while True:
    print 'waitting for connection...'
    tcpCliSock,addr=tcpSerSock.accept()
    print '...connected from:',addr
    
    
    while True:
        try:
            data=tcpCliSock.recv(BUFSIZ)
            data=binascii.b2a_hex(data)
        except:
            print "Error receiving:"
            break 
	
	print "data is : " + data 
        if not data:
            break
        if rec_flag==0:
            if data=='ff':  
                buffer[:]=[]
                rec_flag=1
                i=0
        else:
            if data=='ff':
                rec_flag=0
                if i==3:
                    print 'Got data',str(buffer),"\r"
                    Communication_Decode();
                i=0
            else:
                buffer.append(data)
                i+=1
   
        #print(binascii.b2a_hex(data))
    tcpCliSock.close()
tcpSerSock.close()
    

