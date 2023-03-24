import time

import server_message as sm

messagesArray = []


def receiveMessage(socket, stage=None):
    global messagesArray
    pattern = b'\a\b'
    message = b''
    socket.settimeout(1)
    try:
        data = socket.recv(1024)
        if b'RECHARGING\a\b' in data:
            messagesArray += data.split(pattern)
            messagesArray.pop(-1)
            messagesArray.remove(b'RECHARGING')
            try:
                socket.settimeout(5)
                data = socket.recv(1024)
                messagesArray += data.split(pattern)
                messagesArray.pop(-1)
                if b'FULL POWER' in messagesArray:
                    messagesArray.remove(b'FULL POWER')
                    if not messagesArray:
                        data = socket.recv(1024)
                        messagesArray += data.split(pattern)
                        messagesArray.pop(-1)
                    return
                else:
                    sm.SERVER_LOGIC_ERROR(socket)
            except:
                socket.close()
        smth = data.split(b'\a\b')
        if stage == 'ACCEPT_CLIENT_USERNAME':
            if len(smth[0]) > 16:
                sm.SERVER_SYNTAX_ERROR(socket)
        elif stage == 'SERVER_PICK_UP':
            if len(smth[0]) > 96:
                sm.SERVER_SYNTAX_ERROR(socket)
        elif stage == 'coordinates' and ((smth[0] != b'RECHARGING') and (smth[0] != b'FULL POWER')):
            if len(smth[0]) > 8:
                sm.SERVER_SYNTAX_ERROR(socket)
    except:
        socket.close()
    message += data
    if data.endswith(pattern):
        messagesArray = data.split(pattern)
        messagesArray.pop(-1)
    else:
        while not message.endswith(pattern):
            socket.settimeout(1)
            try:
                data = socket.recv(1024)
            except:
                socket.close()
            message += data
        messagesArray = message.split(pattern)
        messagesArray.pop(-1)


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


def obstacles(socket, direction=None, coordinates=None):
    if direction == 'R':
        if coordinates[1] < 0:
            sm.SERVER_TURN_LEFT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_MOVE(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_TURN_RIGHT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
        elif coordinates[1] > 0:
            sm.SERVER_TURN_RIGHT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_MOVE(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_TURN_LEFT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
    elif direction == 'L':
        if coordinates[1] > 0:
            sm.SERVER_TURN_LEFT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_MOVE(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_TURN_RIGHT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
        elif coordinates[1] < 0:
            sm.SERVER_TURN_RIGHT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_MOVE(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
            sm.SERVER_TURN_LEFT(socket)
            if not messagesArray:
                receiveMessage(socket, 'coordinates')
                messagesArray.pop(0)
            else:
                messagesArray.pop(0).decode()
    else:
        sm.SERVER_TURN_RIGHT(socket)
        if not messagesArray:
            receiveMessage(socket, 'coordinates')
            messagesArray.pop(0)
        else:
            messagesArray.pop(0).decode()
        sm.SERVER_MOVE(socket)
        if not messagesArray:
            receiveMessage(socket, 'coordinates')
            messagesArray.pop(0)
        else:
            messagesArray.pop(0).decode()
        sm.SERVER_TURN_LEFT(socket)
        if not messagesArray:
            receiveMessage(socket, 'coordinates')
            messagesArray.pop(0)
        else:
            messagesArray.pop(0).decode()
    sm.SERVER_MOVE(socket)
    if not messagesArray:
        receiveMessage(socket, 'coordinates')
        coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
    else:
        coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
    sm.SERVER_MOVE(socket)
    if not messagesArray:
        receiveMessage(socket, 'coordinates')
        coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
    else:
        coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
    return defineDirection(coordinates, coordinates2), coordinates2


def hashName(name):
    return (sum(ord(c) for c in name) * 1000) % 65536


def recieveCoordinate(string, socket):
    if '.' in string or string[-1].isspace():
        sm.SERVER_SYNTAX_ERROR(socket)
    return tuple(map(int, string.split()[1:]))


def algorithm(socket, coordinates=None, direction=None):
    if coordinates == (0, 0):
        sm.SERVER_PICK_UP(socket)

    if direction is None:
        sm.SERVER_MOVE(socket)
        if not messagesArray:
            receiveMessage(socket, 'coordinates')
            coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
        else:
            coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
        sm.SERVER_MOVE(socket)
        if not messagesArray:
            receiveMessage(socket, 'coordinates')
            coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
        else:
            coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
        if coordinates == coordinates2:
            direction, coordinates2 = obstacles(socket)
        else:
            direction = defineDirection(coordinates, coordinates2)
        algorithm(socket, coordinates2, direction)

    if coordinates[0] != 0:
        if direction == 'R':
            if coordinates[0] < 0:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                if coordinates == coordinates2:
                    direction, coordinates2 = obstacles(socket)
                algorithm(socket, coordinates2, direction)
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                algorithm(socket, coordinates, 'L')

        if direction == 'L':
            if coordinates[0] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                if coordinates == coordinates2:
                    direction, coordinates2 = obstacles(socket)
                algorithm(socket, coordinates2, direction)
                algorithm(socket, coordinates2, direction)

        if direction == 'U':
            if coordinates[0] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'L')

        if direction == 'D':
            if coordinates[0] < 0:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'L')

    if coordinates[1] != 0:
        if direction == 'R':
            if coordinates[1] < 0:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'D')

        if direction == 'L':
            if coordinates[1] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'D')

        if direction == 'U':
            if coordinates[1] < 0:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                if coordinates == coordinates2:
                    direction, coordinates2 = obstacles(socket)
                algorithm(socket, coordinates2, direction)
                algorithm(socket, coordinates2, direction)
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'D')

        if direction == 'D':
            if coordinates[1] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    recieveCoordinate(messagesArray.pop(0).decode(), socket)
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket, 'coordinates')
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                else:
                    coordinates2 = recieveCoordinate(messagesArray.pop(0).decode(), socket)
                if coordinates == coordinates2:
                    direction, coordinates2 = obstacles(socket)
                algorithm(socket, coordinates2, direction)
