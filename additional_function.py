import server_message as sm


def decodeMessage(message):
    smth = message.decode()
    index = smth.find('\a\b')
    return smth[:index]


def defineDirection(tup1, tup2):
    if tup1[1] == tup2[1]:
        if tup1[0] > tup2[0]:
            return 'L'
        if tup1[0] < tup2[0]:
            return 'R'
    if tup1[0] == tup2[0]:
        if tup1[1] > tup2[1]:
            return 'D'
        if tup1[1] < tup2[1]:
            return 'U'


def hashName(name):
    return (sum(ord(c) for c in name) * 1000) % 65536


def recieveCoordinate(string):
    return tuple(map(int, string.split()[1:]))


def algorithm(socket, coordinates=None, direction=None):
    if coordinates == (0, 0):
        socket.send(b'105 GET MESSAGE\a\b')
        socket.recv(1024)
        socket.send(b'106 LOGOUT\a\b')
        socket.close()

    if direction is None:
        sm.SERVER_MOVE(socket)
        coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
        sm.SERVER_MOVE(socket)
        coordinates2 = recieveCoordinate(decodeMessage(socket.recv(1024)))
        direction = defineDirection(coordinates, coordinates2)
        algorithm(socket, coordinates2, direction)

    if coordinates[0] != 0:
        if direction == 'R':
            if coordinates[0] < 0:
                sm.SERVER_MOVE(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, direction)
            else:
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'L')

        if direction == 'L':
            if coordinates[0] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                sm.SERVER_MOVE(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, direction)
            else:
                sm.SERVER_MOVE(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, direction)

        if direction == 'U':
            if coordinates[0] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_TURN_LEFT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'L')

        if direction == 'D':
            if coordinates[0] < 0:
                sm.SERVER_TURN_LEFT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_TURN_RIGHT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'L')

    if coordinates[1] != 0:
        if direction == 'R':
            if coordinates[1] < 0:
                sm.SERVER_TURN_LEFT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_TURN_RIGHT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'D')

        if direction == 'L':
            if coordinates[1] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_TURN_LEFT(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'D')

        if direction == 'U':
            if coordinates[1] < 0:
                sm.SERVER_MOVE(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, direction)
            else:
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'D')

        if direction == 'D':
            if coordinates[1] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                sm.SERVER_TURN_RIGHT(socket)
                recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_MOVE(socket)
                coordinates = recieveCoordinate(decodeMessage(socket.recv(1024)))
                algorithm(socket, coordinates, direction)
