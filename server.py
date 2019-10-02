import socket
from threading import Thread
import os

clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # clean up
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        filename = ''
        file_buffer = b''
        while True:
            # try to read 1024 bytes from user
            # this is blocking call, thread will be paused here
            data = self.sock.recv(1024)
            if data:
                if len(filename) == 0:
                    filename = data.decode()
                    print("Start receiving file %s" % filename)
                else:
                    file_buffer += data
            else:
                copy = 1
                dot = filename.index('.')
                new_filename = filename
                if os.path.isfile(filename):
                    new_filename = filename[:dot] + '_copy%s' + filename[dot:]
                    while os.path.isfile(new_filename % str(copy)):
                        copy += 1
                    new_filename = new_filename % str(copy)
                file = open(new_filename, 'wb')
                file.write(file_buffer)
                print("%s received" % new_filename)
                # if we got no data – client has disconnected
                self._close()
                # finish the thread
                return


def main():
    next_name = 1

    # AF_INET – IPv4, SOCK_STREAM – TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address; in OS address will be reserved after app closed for a while
    # so if we close and imidiatly start server again – we'll get error
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen to all interfaces at 8800 port
    sock.bind(('', 3333))
    sock.listen()
    while True:
        # blocking call, waiting for new client to connect
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        # start new thread to deal with client
        ClientListener(name, con).start()


if __name__ == "__main__":
    main()
