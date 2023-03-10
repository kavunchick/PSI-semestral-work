import additional_function as ad

KEYS = {0: (23019, 32037), 1: (32037, 29295), 2: (18789, 13603), 3: (16443, 29533), 4: (18189, 21952)}


def SERVER_CONFIRMATION(socket, name, key_id):
    number = ad.hashName(name) + int(KEYS[key_id][0]) % 65536
    answer = f'{number}\a\b'
    socket.send(answer.encode())


def SERVER_KEY_OUT_OF_RANGE_ERROR(socket):
    socket.send(b'303 KEY OUT OF RANGE\a\b')
    socket.close()


def SERVER_SYNTAX_ERROR(socket):
    socket.send(b'301 SYNTAX ERROR\a\b')
    socket.close()


def ACCEPT_CLIENT_KEY(socket, name, key_id):
    number = (ad.hashName(name) + KEYS[key_id][1]) % 65536
    clientID = socket.recv(1024)
    clientID_decode = clientID.decode()
    index = clientID_decode.find('\a\b')
    clientID_decode = int(clientID_decode[:index])
    if clientID_decode == number:
        socket.send(b'200 OK\a\b')
    else:
        socket.send(b'300 LOGIN FAILED\a\b')
        socket.close()


def SERVER_MOVE(socket):
    socket.send(b'102 MOVE\a\b')


def SERVER_TURN_LEFT(socket):
    socket.send(b'103 TURN LEFT\a\b')


def SERVER_TURN_RIGHT(socket):
    socket.send(b'104 TURN RIGHT\a\b')


def ACCEPT_CLIENT_USERNAME(socket):
    BotName = socket.recv(1024)
    BotName_decode = BotName.decode()
    index = BotName_decode.find('\a\b')
    return BotName_decode[:index], BotName


def SERVER_KEY_REQUEST(socket):
    socket.send(b'107 KEY REQUEST\a\b')
    KeyID = socket.recv(1024)
    if not ad.decodeMessage(KeyID).isnumeric():
        SERVER_SYNTAX_ERROR(socket)
    KeyID = int(ad.decodeMessage(KeyID))
    if KeyID > 4 or KeyID < 0:
        SERVER_KEY_OUT_OF_RANGE_ERROR(socket)
    return KeyID
