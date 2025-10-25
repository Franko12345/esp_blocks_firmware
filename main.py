import network
import usocket as socket
from request_parser import parse_request
import esp
import time
import _thread
from machine import Pin
import machine


machine.freq(240000000)
addr = ""
def do_connect():
    global addr
    import machine, network

    network.WLAN(network.AP_IF).active(False)
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.config(dhcp_hostname="esp_kit")


    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('SemMedoDeSerFeliz', 'estrela13')
        while not wlan.isconnected():
            machine.idle()
    addr = wlan.ifconfig()
    print('network config: ', addr)

do_connect()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(50)

led = Pin(2, Pin.OUT)


def recieve_code(conn, args):
    print(args)

    conn.send("Code successfully recieved!")
    conn.close()


routes = {
    "/recieve" : recieve_code
    #"/set-color": set_static_color,
    #"/dynamic": set_dynamic_animation
    }

#variables = {
#    "STATE": lambda: "true" if state == "on" else "false",
#    "MODE": lambda: str(not active_animation).lower(),
#    "COLOR": lambda: "#" + open("color.txt", "r").read()
#}


while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = parse_request(request)
    conn.send("Size recieved".encode("utf-8"))
    conn.close()
    
    conn, addr = s.accept()
    request = conn.recv(1024 + int(request["args"]["size"]))
    request = parse_request(request)
    conn.send(request["body"].encode("utf-8"))
    conn.close()
#    try:
#
#        request = parse_request(request)
#
#        led.toggle()
#
#        if request["url"] in routes:
#            time.sleep(.05)
#            _thread.start_new_thread(routes[request["url"]], (conn, request["args"]))
#
#        else:
#            conn.send("pong")
#            conn.close()
#            
#    except Exception as e:
#        conn.send(str(e).encode("utf-8"))
#        conn.close()
