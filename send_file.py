import os
import socket  # Import socket module
import sys
import time
import progressbar

s = socket.socket()  # Create a socket object
file = sys.argv[1]
host = sys.argv[2]  # Get local machine name
port = int(sys.argv[3])  # Reserve a port for your service.

s.connect((host, port))  # establish connection
print('Sending filename...')
s.send(file.encode())  # send filename
time.sleep(0.1)
f = open(file, 'rb')
file_size = os.stat(file).st_size
l = f.read(1024)
print('Sending...')
bar = progressbar.ProgressBar(file_size).start()
sent = 0
while (l):
    s.send(l)  # send file with chunks of 1024 bytes
    bar.update(sent)
    time.sleep(0.1)
    sent += 1024
    l = f.read(1024)
f.close()  # close file when no more data
bar.finish()
print("Done Sending\n")
s.close()  # close connection
