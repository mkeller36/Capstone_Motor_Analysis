# Author: Michael Keller
# Title: Motor Analysis
# Interpreter: Python 3.7.6

# imports
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.axis as ax
import pandas as pd

# Var setup 
WheelDiameter = 5.4 #inch 
mass = float(240) # OZ = 15 lbs
conversion = 0.00094697 # Oz-In to ft-lbs
conversion2 = 0.056818181818184 # in/s^2 to mph/s
activewheels = [3.0,4.0,5.0,6.0]
slopeangle = [0.0,5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,90.0]
approachAngle = [0.0,5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,90.0]
gravity = 32.2 #ft/s^2

# Creating Class (Marx would not approve)
class motor:
  def __init__(self, rpm, torque, speed, accel):
    self.motor = motor
    self.rpm = rpm
    self.torque = torque
    self.speed = speed
    self.accel = accel

# Setting opjects
motor1 = motor(313,416.6,0,0)
motor2 = motor(437,305.5,0,0)
motor3 = motor(612,222.0,0,0)
motor4 = motor(1621,97.2,0,0)

# rpm to speed - mph
motor1.speed = math.pi*WheelDiameter*motor1.rpm*conversion
motor2.speed = math.pi*WheelDiameter*motor2.rpm*conversion
motor3.speed = math.pi*WheelDiameter*motor3.rpm*conversion
motor4.speed = math.pi*WheelDiameter*motor4.rpm*conversion

# Acceleration on flat ground - mph/s
motor1.accel = (motor1.torque/(WheelDiameter/2))*conversion2 
motor2.accel = (motor2.torque/(WheelDiameter/2))*conversion2 
motor3.accel = (motor3.torque/(WheelDiameter/2))*conversion2 
motor4.accel = (motor4.torque/(WheelDiameter/2))*conversion2 

# Set arrays 
rpm_arr = [motor1.rpm,motor2.rpm,motor3.rpm,motor4.rpm]
torque_arr = [motor1.torque,motor2.torque,motor3.torque,motor4.torque]
speed_arr = [motor1.speed,motor2.speed,motor3.speed,motor4.speed]
accel_arr = [motor1.accel,motor2.accel,motor3.accel,motor4.accel]

# Plot torque to RPM
plt.figure(1)
plt.subplot(1, 2, 1,)
relation = np.polyfit(rpm_arr,torque_arr,2)
plt.plot(rpm_arr,torque_arr,'o')
plt.xlabel('RPM',fontsize=22)
plt.ylabel('torque (Oz-In)',fontsize=22)
plt.title('RPM vs torque',fontsize=22)
plt.text(600,350,str(round(relation[0],5))+'$x^{2} + $' + str(round(relation[1],3)) + 'x + '+ str(round(relation[2],3)),fontsize=18)
plt.grid(b=None, which='major', axis='both')

# Plot Speed to RPM
plt.subplot(1, 2, 2) 
plt.plot(rpm_arr,speed_arr,'o-')
plt.xlabel('RPM',fontsize=22)
plt.ylabel('speed (mph)',fontsize=22)
plt.title('RPM vs Speed',fontsize=22)
relation = np.polyfit(rpm_arr,speed_arr,1)
plt.text(1000,10,str(round(relation[0],3)) + 'x + '+ str(round(relation[1],5)),fontsize=18)
plt.grid(b=None, which='major', axis='both')
plt.show()

# Possible climb angle 
# Theory: active wheels * torque * wheel diameter  = mass * gravity * sin(slope angle)
degsperwheel = []
for i in range(len(activewheels)):
    wheels = activewheels[i]
    #print('----------------' + str(wheels) + ' Active Wheels' + '----------------')
    for i in range(len(torque_arr)):
        torque = torque_arr[i]
        dem = mass*gravity*WheelDiameter/2
        num = wheels*torque
        theta = num/dem
        maxsloperads = math.asin(theta)
        maxslopedegs = round((180/math.pi)*maxsloperads,2)
        degsperwheel.append(maxslopedegs)
        #print('for ' + str(rpm_arr[i]) + ' motor, max slope is ' + str(maxslopedegs))

# Splitting list by motor 
degsperwheel313 = degsperwheel[::4]
degsperwheel437 = degsperwheel[1::4]
degsperwheel612 = degsperwheel[2::4]
degsperwheel1621 = degsperwheel[3::4]

# Plotting max slope vs active wheels
plt.figure(2)
plt.plot(activewheels,degsperwheel313,'r-',activewheels,degsperwheel437,'b-',activewheels,degsperwheel612,'g-',activewheels,degsperwheel1621,'k-')
plt.legend(['313 RPM','437 RPM','612 RPM','1621 RPM'],fontsize=16)
plt.xlabel('Active wheels',fontsize=22)
plt.ylabel('Max ascent angle (degrees)',fontsize=22)
plt.title('Active Wheels vs Max ascent angle',fontsize=22)
plt.grid(b=None, which='major', axis='both',)
plt.show()


# Splitting list by active wheels 
wheels6 = degsperwheel[len(degsperwheel)-4:len(degsperwheel)]
wheels5 = degsperwheel[len(degsperwheel)-8:len(degsperwheel)-4]
wheels4 = degsperwheel[len(degsperwheel)-12:len(degsperwheel)-8]
wheels3 = degsperwheel[len(degsperwheel)-16:len(degsperwheel)-12]

# Plotting rpm vs angle 
plt.figure(3)
plt.plot(rpm_arr,wheels3,'r-',rpm_arr,wheels4,'b-',rpm_arr,wheels5,'g-',rpm_arr,wheels6,'k-')
plt.legend(['3 Wheels','4 Wheels','5 Wheels','6 Wheels'],fontsize=16)
plt.xlabel('RPM',fontsize=22)
plt.ylabel('Max ascent angle (degrees)',fontsize=22)
plt.title('RPM vs Max ascent angle',fontsize=22)
plt.grid(b=None, which='major', axis='both')
plt.show()

# torque needed at different angle to go up incline 
# Theory: torque*radius = mass*gravity*sin(incline angle)*cos(angle of approach)
# Assume all wheels active for this 
torqueNeeded = []
activewheels = 6.0
for i in range(len(slopeangle)):
    slope = slopeangle[i]
    #print('----------------' + str(slope) + ' Degree Slope ' + '----------------')
    for i in range(len(approachAngle)):
        approach = approachAngle[i]
        torque = round(((mass*gravity*np.sin(slope*np.pi/180)*np.cos(approach*np.pi/180))*(WheelDiameter/2))/activewheels,2)
        torqueNeeded.append(torque)
        #print('for ' + str(approachAngle[i]) + ' approach, torque needed is ' + str(torque))

mult = []
for i in range(len(approachAngle)):
    mult.append(i*len(np.round(approachAngle)))

# Splitting list by slope angle 
torqueNeeded0 =  torqueNeeded[mult[0]:mult[1]]  
torqueNeeded5 =  torqueNeeded[mult[1]:mult[2]]   
torqueNeeded10 = torqueNeeded[mult[2]:mult[3]]  
torqueNeeded15 = torqueNeeded[mult[3]:mult[4]]  
torqueNeeded20 = torqueNeeded[mult[4]:mult[5]]   
torqueNeeded25 = torqueNeeded[mult[5]:mult[6]]   
torqueNeeded30 = torqueNeeded[mult[6]:mult[7]]   
torqueNeeded35 = torqueNeeded[mult[7]:mult[8]]   
torqueNeeded40 = torqueNeeded[mult[8]:mult[9]]  
torqueNeeded45 = torqueNeeded[mult[9]:mult[10]] 
torqueNeeded50 = torqueNeeded[mult[10]:mult[11]]
torqueNeeded55 = torqueNeeded[mult[11]:mult[12]] 
torqueNeeded60 = torqueNeeded[mult[12]:mult[13]]
torqueNeeded65 = torqueNeeded[mult[13]:mult[14]] 
torqueNeeded70 = torqueNeeded[mult[14]:mult[15]] 
torqueNeeded75 = torqueNeeded[mult[15]:mult[16]] 
torqueNeeded80 = torqueNeeded[mult[16]:mult[17]] 
torqueNeeded85 = torqueNeeded[mult[17]:mult[18]] 
torqueNeeded90 = torqueNeeded[mult[18]:mult[19]] 

# Plot of Torque vs approach angle 
plt.figure(4)
plt.plot(approachAngle, torqueNeeded0, 'k',approachAngle, torqueNeeded5, 'b',approachAngle, torqueNeeded10, 'g',approachAngle, torqueNeeded15, \
    'r',approachAngle, torqueNeeded20, 'c',approachAngle, torqueNeeded25, 'm',approachAngle, torqueNeeded30, 'y'\
        ,approachAngle, torqueNeeded35, 'k',approachAngle, torqueNeeded40, 'b',approachAngle, torqueNeeded45, 'g',\
            approachAngle, torqueNeeded50, 'c',approachAngle, torqueNeeded55, 'm',approachAngle, torqueNeeded60, 'y',\
                approachAngle, torqueNeeded65, 'k',approachAngle, torqueNeeded70, 'b',approachAngle, torqueNeeded75, 'g',\
                    approachAngle, torqueNeeded80, 'c',approachAngle, torqueNeeded85, 'm',approachAngle, torqueNeeded90, 'y')
plt.title('Torque Required per approach angle for ' + str(round(activewheels)) + ' wheels',fontsize=22)
plt.legend(['0 Degrees','5 Degrees','10 Degrees','15 Degrees','20 Degrees','25 Degrees','30 Degrees','35 Degrees','40 Degrees','45 Degrees',\
     '50 Degrees','55 Degrees','60 Degrees','65 Degrees','70 Degrees','75 Degrees','80 Degrees','85 Degrees','90 Degrees'],title = 'Incline Angle',fontsize=14)
plt.xlabel('Approach Angle (Degrees)',fontsize=22)
plt.ylabel('Torque Needed (Oz-In)',fontsize=22)
plt.grid(b=None, which='major', axis='both')
plt.show()

# Max ascent angle for variying coeffiecents of friction 
# Theory: torque <= Mass*gravity*coeffiecents of friction/number of wheels 


# Data Frame print 
# Set Data Values
data1 = np.array([
[motor1.rpm, motor1.speed, motor1.accel,degsperwheel313[3]],
[motor2.rpm, motor2.speed, motor2.accel,degsperwheel437[3]],
[motor3.rpm, motor3.speed, motor3.accel,degsperwheel612[3]],
[motor4.rpm, motor4.speed, motor4.accel,degsperwheel1621[3]]
])

# Set Column Vales 
colNames = ['Motor RPM', 'Motor Speed (mph)', 'Motor Acceleration (mph/s)','Max Climb Angle (degrees)']

# Create and print data frame 
print('For chassis of mass ' + str(round(mass)) + ' Oz')
df = pd.DataFrame(data = data1,columns=colNames )
print(df)

