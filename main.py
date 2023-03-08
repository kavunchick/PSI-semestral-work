import socket
import threading
import _thread as th

print_lock = threading.Lock()

HOST = "127.0.0.1"
PORT = 5000


def connection(socket):
    while True:
        message = socket.recv(1024)
        if not message:
            try:
                socket.send(b'SYNTAX ERROR\\a\\b')
            except BrokenPipeError:
                print('Client closed the connection.')
                break
        else:
            socket.send(message)


def main():
    Lsocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    Lsocket.bind((HOST, PORT))
    print(f'Lsocket binded to {HOST, PORT}')
    Lsocket.listen()
    print(f'Listen {HOST, PORT}')
    while True:
        NewSocket, address = Lsocket.accept()
        print_lock.acquire()
        print('Connected to :', address[0], ':', address[1])
        th.start_new_thread(connection, (NewSocket,))
    Lsocket.close()

main()
