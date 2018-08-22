import zmq
import sys
import json
import time
import random

port = '5555'
host = 'localhost'

if len(sys.argv) > 1:
    host = sys.argv[1]

if len(sys.argv) > 2:
    port = sys.argv[2]

context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect('tcp://%s:%s' % (host, port))

print ('''available operations: +, -, *, /, ^
    use: number1 number2 operator
    example: 1 6 +
    ''')

while True:
    operation = input('>>> operation: ').strip().replace(' ', '?')

    socket.send_string('op?' + operation)
    message = socket.recv().decode('utf-8').split('?')
    d = message[1]
    print('Operation result is {}'.format(d))