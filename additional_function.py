import server_message as sm

messagesArray = []


def receiveMessage(socket):
    message = b''
    data = socket.recv(1024)
    message += data
    global messagesArray
    if b'\a\b' in data:
        pattern = b'\a\b'
        messagesArray = data.split(pattern)
        messagesArray.pop(-1)
    else:
        while b'\a\b' not in message:
            data = socket.recv(1024)
            message += data
        messagesArray.append(message[:-2])



def decodeMessage(message):
    smth = message.decode()
    index = smth.find('\a\b')
    return smth[:index]


def defineDirection(tup1, tup2):
    print(tup1, tup2)
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
        if not messagesArray:
            receiveMessage(socket)
            messagesArray.pop(0)
        else:
            messagesArray.pop(0).decode()
        socket.send(b'106 LOGOUT\a\b')
        socket.close()

    if direction is None:
        sm.SERVER_MOVE(socket)
        if not messagesArray:
            receiveMessage(socket)
            coordinates = recieveCoordinate(messagesArray.pop(0).decode())
        else:
            coordinates = recieveCoordinate(messagesArray.pop(0).decode())
        sm.SERVER_MOVE(socket)
        if not messagesArray:
            receiveMessage(socket)
            coordinates2 = recieveCoordinate(messagesArray.pop(0).decode())
        else:
            coordinates2 = recieveCoordinate(messagesArray.pop(0).decode())
        direction = defineDirection(coordinates, coordinates2)
        algorithm(socket, coordinates2, direction)

    if coordinates[0] != 0:
        if direction == 'R':
            if coordinates[0] < 0:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, direction)
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                algorithm(socket, coordinates, 'L')

        if direction == 'L':
            if coordinates[0] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    messagesArray.pop(0)
                else:
                    messagesArray.pop(0).decode()
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, direction)

        if direction == 'U':
            if coordinates[0] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'L')

        if direction == 'D':
            if coordinates[0] < 0:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'R')
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'L')

    if coordinates[1] != 0:
        if direction == 'R':
            if coordinates[1] < 0:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'D')

        if direction == 'L':
            if coordinates[1] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_TURN_LEFT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'D')

        if direction == 'U':
            if coordinates[1] < 0:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, direction)
            else:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'D')

        if direction == 'D':
            if coordinates[1] < 0:
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                sm.SERVER_TURN_RIGHT(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, 'U')
            else:
                sm.SERVER_MOVE(socket)
                if not messagesArray:
                    receiveMessage(socket)
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                else:
                    coordinates = recieveCoordinate(messagesArray.pop(0).decode())
                algorithm(socket, coordinates, direction)
