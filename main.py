import socket
import threading
import server_message as sm
import additional_function as ad

HOST = '127.0.0.1'
PORT = 6000


def connection(socket):
    try:
        print('===========NEW CONNECTION=======')
        BotName_decode = sm.ACCEPT_CLIENT_USERNAME(socket)
        KeyID = sm.SERVER_KEY_REQUEST(socket)
        sm.SERVER_CONFIRMATION(socket, BotName_decode, KeyID)
        sm.ACCEPT_CLIENT_KEY(socket, BotName_decode, KeyID)
        ad.algorithm(socket)
    except:
        pass


def main():
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as Lsocket:
        Lsocket.bind((HOST, PORT))
        Lsocket.listen()
        while True:
            NewSocket, address = Lsocket.accept()
            thread = threading.Thread(target=connection, args=(NewSocket,))
            thread.start()


if __name__ == '__main__':
    main()
