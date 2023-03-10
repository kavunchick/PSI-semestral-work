import socket
import threading
import server_message as sm
import additional_function as ad

print_lock = threading.Lock()

HOST = "127.0.0.1"
PORT = 4000


def connection(socket):
    BotName_decode, BotName = sm.ACCEPT_CLIENT_USERNAME(socket)
    KeyID = sm.SERVER_KEY_REQUEST(socket)
    sm.SERVER_CONFIRMATION(socket, BotName_decode, KeyID)
    sm.ACCEPT_CLIENT_KEY(socket, BotName_decode, KeyID)
    ad.algorithm(socket)


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
        try:
            thread = threading.Thread(target=connection, args=(NewSocket,))
            thread.start()
        except Exception as e:
            print(e)
        finally:
            print_lock.release()
    Lsocket.close()



main()
