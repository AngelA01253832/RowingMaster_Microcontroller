import usocket as socket
import time
from machine import Pin,Timer 
import network
import esp
esp.osdebug(None)
import gc

gc.collect()

hallSensor = Pin(12, Pin.IN) #Hall sensor read
led = Pin(13,Pin.OUT) #Output LED

totalDistance = 0.0
totalCalories = 0 

def addDistance():
    global totalDistance
    global totalCalories
    startTime = time.time()
    if hallSensor.value() > 0:
        led.off()
        totalDistance += 0.0
        totalCalories += 0
    else:
        led.on()
        totalDistance += 1.25
        finalTime = time.time()
        timeLap = startTime - finalTime
        totalCalories += int(round((1.25/timeLap)**3)*9.6367 + 300,0)
tim = Timer(1)
tim.init(period=100, mode=Timer.PERIODIC, callback=lambda t:
    addDistance()
)


# ssid = 'INFINITUM2FEF'
# password='2115134343'

#zepeda test
# ssid = 'HUAWEI P40 lite'
# password='pepe123pepe'

#access point
ssid = 'RowingMaster'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid = ssid, password = password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

def WorkoutInterface():
    html = """<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv=\"refresh"\ content="1">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <!-- CSS only -->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.2/font/bootstrap-icons.css">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
                <title>Rowing Master</title>
                </head>
            <body>
                <h1>Distancia:"""+str(round(totalDistance,2))+""" km</h1>
                <h1>Distancia:"""+str(totalCalories)+""" calorias</h1>
                <!-- JavaScript Bundle with Popper -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
            </body>
            </html>        
        """
    return html

# #Socket configuration
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    response = WorkoutInterface()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
    print(addDistance)
  except OSError as e:
    conn.close()
    print('Connection closed')
