import zmq
import time
import sys
import socket as spython
import json

port = '5555'

def get_ip():
    s = spython.socket(spython.AF_INET, spython.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return (ip)

op_servers = {}

if len(sys.argv) > 1:
    port = sys.argv[1]

context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind('tcp://*:%s' % port)

print ('servidor ejecutandose en ', get_ip(), ':', port)

while True:
    message = socket.recv().decode('utf-8').split('?')
    header =  message[0]
    print (message)
    if (header == 'addme'):
        op_servers[message[1]] = [message[2], message[3]]
        socket.send_string('ok')
    elif (header == 'op'):
        if message[3] in op_servers:
            socket_ = context.socket(zmq.REQ)
            socket_.connect('tcp://%s:%s' % (op_servers[message[3]][0], op_servers[message[3]][1]))
            socket_.send_string(message[3] + '?' + message[1] + '?' + message[2])
            message1 = socket_.recv()
            socket_.close()
            socket.send(message1)
        else:
            socket.send_string('result?There is not a valid operation');

