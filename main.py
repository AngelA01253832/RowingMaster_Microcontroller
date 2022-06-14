import usocket as socket
from hcsr04 import HCSR04
from machine import Pin,Timer 
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

#Microcontroller variables
ultrasonicSensor = HCSR04(trigger_pin=2 , echo_pin=0, echo_timeout_us=1000000 )#Ultrasonic sensor (intensity)
hallSensor = Pin(12, Pin.IN) #Hall sensor read
ledSuccess = Pin(15,Pin.OUT) #Output LED (Test sensor)
ledError = Pin(13,Pin.OUT) #Output LED (Test sensor)

#Init variables
totalDistance = 0.0
totalCalories = 0.0
totalIntensity = 0.0
timer = 0
distance = 0
direction = True


def addDistance():
    global totalDistance, totalCalories
    if hallSensor.value() > 0:
        totalDistance += 0.0
        totalCalories += 0.0
    elif hallSensor.value() < 1:
        totalDistance += 0.75
        totalCalories += 0.01
    
def rowingTime():
    global timer, direction
    if direction:
        timer += 1
def addIntensity():
    global totalIntensity
    totalIntensity = ultrasonicSensor.distance_cm()
#     if distance > 10:
#         totalIntensity = 0 * 10
#     elif distance < 2:
#         totalIntensity = 10 * 10
#     else:
#         totalIntensity = distance * 10
    
def timerFormat(seconds):
    hour = seconds//3600
    hour1 = seconds % 3600
    minute = hour1 // 60
    second = hour1 % 60
    return(f'{hour:02d}:{minute:02d}:{second:02d}')


timDistance = Timer(1)
timIntenstity = Timer(1)
tim = Timer(1)
timDistance.init(period=100, mode=Timer.PERIODIC, callback=lambda t:addDistance())
timIntenstity.init(period=100, mode=Timer.PERIODIC, callback=lambda t:addIntensity())
tim.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: rowingTime())


ssid = 'INFINITUM2FEF'
password='2115134343'
wlan = network.WLAN(network.STA_IF)

wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    pass

print('Connection successful')
ledSuccess.on()
print(wlan.ifconfig())

#zepeda test
# ssid = 'HUAWEI P40 lite'
# password='pepe123pepe'

# # #Socket configuration
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


def WorkoutInterface():
    html = """<!DOCTYPE html>
                <html lang="en">
                  <head>
                    <meta charset="UTF-8" />
                    <meta http-equiv=\"refresh"\ content="1">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous"/>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.2/font/bootstrap-icons.css"/>
                  </head>
                  <body style=" background:linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('https://w0.peakpx.com/wallpaper/799/387/HD-wallpaper-by-kayak-nature-river-mountains-kayak.jpg') no-repeat center center fixed ; background-size: cover; color:#FFF;">
                  <div class="d-flex justify-content-center"><i style="font-size:x-large;" class="bi bi-list "> Rowing Master</i></div>
                  <div><div style=" width: 200px; height: 200px; border-radius: 50%; background-color: transparent; margin: 20vh auto 0; border-style: solid; border-color:#FFF; display:flex; justify-content:center; align-items:center;" class="text-center" >
                        <div><h1>"""+str(timerFormat(timer))+"""</h1><i style="font-size: larger;" class="bi bi-clock">Time</i> </div></div>
                        <div class="d-flex justify-content-around" style="margin-top: 25px;">
                          <div style="text-align: center"><h1>"""+str(round(totalCalories,0))+"""</h1><i style="font-size: larger;" class="bi bi-heart-pulse"> Cals</i></div>
                          <div style="text-align: center"><h1>"""+str(totalIntensity)+""" cm</h1><i style="font-size: larger;" class="bi bi-bar-chart"> Intensity</i></div>
                          <div style="text-align: center"><h1>"""+str(round(totalDistance/1000,2))+"""</h1><i style="font-size: larger;" class="bi bi-geo">Km</i></div>
                          </div></div>
                        <div style="margin-top:10vh" class="d-flex justify-content-center"><a href="/workout=off" class="btn btn-danger">Salir de app </a></div>
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js"integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2"crossorigin="anonymous"></script>
                      </body>
                    </html>
                  </div>
     
        """
    return html

def initInterface():
    html = """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
                    <title>Rowing Master | Home</title>
                </head>
                <title>Rowing Master | Home</title>
                <body class="p-3 mb-2 bg-dark text-white">
                    <h1 class="text-center">Rowing Master | Inicio</h1>
                    <main class="d-flex justify-content-around">
                        <a href="/workout=on" class="btn btn-success">Iniciar entrenamiento</a>
                        <a href="/workout=off" class="btn btn-danger">Salir de app </a>
                    </main>
                </html>"""
    return html

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        req = conn.recv(1024)
        request = str(req)
    
        if request.find('/workout=on') == 6:
            if request.find('/workout=off') == 6:
                ledError.off()
                ledSuccess.off()
                break
            workoutResponse = WorkoutInterface()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(workoutResponse)
            conn.close()
            
        if request.find('/workout=off') == 6:
            ledError.off()
            ledSuccess.off()
            break
        initResponse = initInterface()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(initResponse)
        conn.close()
    except OSError as e:
        ledError.on()
        conn.close()


