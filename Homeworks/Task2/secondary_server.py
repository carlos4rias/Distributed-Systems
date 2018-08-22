import zmq
import time
import sys
import socket as spython
import json
from threading import Thread

port = '5553'
op = '+'

def get_ip():
    s = spython.socket(spython.AF_INET, spython.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return (ip)

if len(sys.argv) > 1:
    port = sys.argv[1]

if len(sys.argv) > 2:
    op = sys.argv[2]


def client(context, server):
    time.sleep(1)
    socket = context.socket(zmq.REQ)
    host = input('ingrese la ip del servidor al que desea conectarse: ')
    portc = input('ingrese el puerto: ')
    connection = 'tcp://' + host + ':' + portc
    socket.connect(connection)
    message = 'addme' + '?' + op + '?' + get_ip() + '?' + port
    socket.send_string(message)
    message = socket.recv().decode('utf-8').split('?')
    if (message[0] == 'ok'):
        print ('the server hooks up succefuly')
    else:
        print (message[0])

    
    socket.close()

def add(a, b):
    return int(a) + int(b)

def multiply(a, b):
    return int(a) * int(b)

def sub(a, b):
    return int(a) - int(b)

def div(a, b):
    return int(a) * 1.0 / int(b)

def server(context):
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:%s' % port)

    print ('servidor ejecutandose en  ', get_ip(), ':', port)
    operations = {'+' : add, '*' : multiply, '/' : div, '-' : sub}
    while True:
        message = socket.recv().decode('utf-8').split('?');

        print (message)

        if message[0] in operations:
            print ("received request: ", message)
            socket.send_string('result?' + str(operations[message[0]](message[1], message[2])))
        else:
            socket.send_string('result?false')

    socket.close()

if __name__ == "__main__":
    context = zmq.Context()
    thread_server = Thread(target = server, args = (context, ) )
    thread_server.start()
    thread_client = Thread(target = client, args = (context, thread_server) )
    thread_client.start()
    thread_server.join()
    thread_client.join()
