import server_message as sm


def decodeMessage(message):
    smth = message.decode()
    index = smth.find('\a\b')
    return smth[:index]


def HashName(name):
    return (sum(ord(c) for c in name) * 1000) % 65536


def RecieveCoordinate(string):
    return tuple(map(int, string.split()[1:]))


def alghoritm(socket):
    sm.SERVER_MOVE(socket)
    while True:
        coordinates = socket.recv(1024)
        coordinates = decodeMessage(coordinates)
        coordinates = RecieveCoordinate(coordinates)
        if coordinates == (0, 0):
            socket.send(b'105 GET MESSAGE\a\b')
            socket.recv(1024)
            socket.send(b'106 LOGOUT\a\b')
            socket.close()
