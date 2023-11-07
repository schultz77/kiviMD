from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from dht import DHT11
import time

import socket
import network

from myKeyPad import KeyPad
import _thread



wifi = network.WLAN(network.STA_IF) # creating wifi network
wifi.active(True)

# configuring temperature/humidity sensor
DHT11Port = 1
myPin = Pin(DHT11Port, Pin.OUT, Pin.PULL_DOWN)
sensorHT11 = DHT11(myPin)
time.sleep(1)
temp_val = 0
hum_val = 0

# configuring relais
RELAIS = 14
ctrlRelais = Pin(RELAIS,Pin.OUT, Pin.PULL_DOWN)
unlock = True
prevLock = False

# configuring OLED display
i2c = I2C(1, sda=Pin(2),scl=Pin(3), freq=400000)
dsp=SSD1306_I2C(128, 64, i2c) # dimensions 128x64 pixels

# configuring inner room button
buttonPin = 21
myButton = Pin(buttonPin, Pin.IN, Pin.PULL_UP)


wifi.connect(secret.wifi, secret.passwd)

cmdFlag = False

while wifi.isconnected() == False:
    # print('waiting for connection . . .')
    dsp.text('connecting . . .', 0, 0)
    time.sleep(1)
    dsp.show()

wifiInfo = wifi.ifconfig()
# print(wifiInfo)
ServerIP = wifiInfo[0]


dsp.fill(0) # clear display
dsp.text('Server IP:', 0, 0)
dsp.text(ServerIP, 0, 10)

ServerPort = 2222
bufferSize = 1024

UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServer.bind((ServerIP, ServerPort))
UDPServer.setblocking(False) # do not wait for a command or message
# print('UDP Server Up and waiting....')

dsp.text('waiting...', 0, 20)
dsp.show()

keyPadObj = KeyPad()
keyString = ''
msgKey = ''

def testCode(code):
    # global tempCode
    if code == "753B":
        message = "success!"
    elif code != "753B#":
        message = "failed!"
    return message

timeStart = None
dispOffFlag = False
dispTimeStart = time.time()

# starting thread for monitoring keypad
#_thread.start_new_thread(keyPadObj.start,())

while True:
    
    if not cmdFlag:
        dsp.fill(0)
        dsp.text('Server IP:', 0, 0)
        dsp.text(ServerIP, 0, 10)
           
    # unlocking using push button -----------------------------
    if myButton.value() == 0:
        cmdFlag = True
        dispTimeStart = time.time()
        dsp.fill(0)
        
        if dispOffFlag:
            dsp.poweron()
            dispOffFlag = False
        
        # print('lock: ', lock)
        # print('prevLock: ', prevLock)
        if unlock != prevLock:
            msg = 'unlocked'
            ctrlRelais.value(1)
            dsp.text(msg, 0, 0)
            time.sleep(1)
            unlock = False
            timeStart = time.time()
    # ---------------------------------------------------------
    
    # unlocking using wifi ------------------------------------
    try:
        message, address = UDPServer.recvfrom(bufferSize)
        # print ('address: ', address[0])
    except OSError:
        pass # No new data. Reuse old data
        # print('pass')
        # cmdFlag = False
    else:
        dispTimeStart = time.time() # restarting timer for switching display off (total: 30s)
        cmd = message.decode("utf-8") # New data has arrived. Use it
        dsp.fill(0)
                          
        if cmd == 'unlock':
            cmdFlag = True 
            msg = 'unlocked'
            ctrlRelais.value(1)
            dsp.text(msg, 0, 0)
            
            msd_enc = msg.encode('utf-8')
            UDPServer.sendto(msd_enc, address) # answering client
            # print(msd_enc, address)
            
            timeStart = time.time() # restarting timer for releasing lock (total: 5s)
            
        if cmd == 'temperature' or cmd == 'humidity':
            temp_hum = str(temp_val) + ',' + str(hum_val)
            temp_hum_enc = temp_hum.encode('utf-8')
            UDPServer.sendto(temp_hum_enc, address)
            # print(temp_hum_enc, address)
            
            timeStart = time.time() # restarting timer for releasing lock (total: 5s)
        
        if dispOffFlag:
            dsp.poweron()
            dispOffFlag = False
    # ---------------------------------------------------------        
    
    # unlocking using keypad ---------------------------------
    # mykey = keyPadObj.key
    mykey = keyPadObj.getKey()
    if mykey is not None:
        dispTimeStart = time.time()
        dsp.fill(0)
        dsp.text('Enter the code', 0, 0)
        dsp.text('folowed by #', 0, 10)
        cmdFlag = True 
        
        if mykey == "#": 
            codeCheck = testCode(keyString)
            # print(codeCheck)
            keyString = ''
            msgKey = ''
            if codeCheck == 'success!':
                # print('relais open')
                ctrlRelais.value(1)
                dsp.fill(0)
                msg = 'unlocked'
                ctrlRelais.value(1)
                # cmdFlag = True 
                
                dsp.text(codeCheck, 0, 0)
                dsp.text(msg, 0, 10)
                timeStart = time.time()
            else:
                dsp.fill(0)
                dsp.text(codeCheck, 0, 0)
                
        elif mykey == "C":
            keyString = ''
            msgKey = ''
        
        elif mykey == "*" and dispOffFlag:
            keyString = ''
            msgKey = ''
            dsp.poweron()
            dispOffFlag = False
        
        elif keyString != '*':
            keyString += mykey
            msgKey += '*' 
            
            dsp.text(msgKey, 0, 35)
        #print('{}'.format(keyString))
    
     # ---------------------------------------------------------
    
    # releaing lock after 5s
    # print(timeStart)
    if timeStart is not None:
        timeElapsed = abs(timeStart - time.time())
        # print(timeElapsed)
        if timeElapsed >= 5:
            dsp.fill(0)
            msg = 'released'
            ctrlRelais.value(0)
            dsp.text(msg, 0, 0)
            unlock = True
            timeStart = None
            cmdFlag = False
            time.sleep(2)
    
    if not dispOffFlag:
        # grabing temperature and humidity values
        time.sleep(.2)
        try:
            sensorHT11.measure()
        except OSError:
            pass 
            
        else:
            tempC = 'Temperature:{}C'.format(sensorHT11.temperature())
            temp_val = sensorHT11.temperature()
            hum = 'Humidity:{}{}'.format(sensorHT11.humidity(), '%')
            hum_val = sensorHT11.humidity()
            #dsp.fill(0)
            
            dsp.text(tempC, 0, 45)
            dsp.text(hum, 0, 55)
            
            dsp.show()
    
    # switching display off after 30s of inactivity
    dispTimeElapsed = abs(dispTimeStart - time.time())
    if dispTimeElapsed > 30:
        dsp.poweroff()
        dispOffFlag = True
        # print('sleep')
        # time.sleep(10)
        # machine.deepsleep(30000)
        machine.lightsleep(10000)
        cmdFlag = False
        
        
