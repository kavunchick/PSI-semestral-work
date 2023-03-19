import additional_function as ad

KEYS = {0: (23019, 32037), 1: (32037, 29295), 2: (18789, 13603), 3: (16443, 29533), 4: (18189, 21952)}


def SERVER_CONFIRMATION(socket, name, keyID):
    number = ad.hashName(name) + int(KEYS[keyID][0]) % 65536
    answer = f'{number}\a\b'
    socket.send(answer.encode())


def SERVER_KEY_OUT_OF_RANGE_ERROR(socket):
    socket.send(b'303 KEY OUT OF RANGE\a\b')
    socket.close()


def SERVER_SYNTAX_ERROR(socket):
    socket.send(b'301 SYNTAX ERROR\a\b')
    socket.close()

def SERVER_PICK_UP(socket):
    socket.send(b'105 GET MESSAGE\a\b')
    if not ad.messagesArray:
        ad.receiveMessage(socket, 'SERVER_PICK_UP')
        ad.messagesArray.pop(0)
    else:
        ad.messagesArray.pop(0).decode()
    socket.send(b'106 LOGOUT\a\b')
    socket.close()

def ACCEPT_CLIENT_KEY(socket, name, key_id):
    number = (ad.hashName(name) + KEYS[key_id][1]) % 65536
    if ad.messagesArray == []:
        ad.receiveMessage(socket)
        clientID = ad.messagesArray.pop(0).decode()
    else:
        clientID = ad.messagesArray.pop(0).decode()
    if len(clientID) > 5 or ' ' in clientID:
        SERVER_SYNTAX_ERROR(socket)
    clientID = int(clientID)

    if clientID == number:
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
    ad.receiveMessage(socket, 'ACCEPT_CLIENT_USERNAME')
    BotName = ad.messagesArray.pop(0).decode()
    if len(BotName) > 16:
        SERVER_SYNTAX_ERROR(socket)
    return BotName


def SERVER_KEY_REQUEST(socket):
    socket.send(b'107 KEY REQUEST\a\b')
    if ad.messagesArray == []:
        ad.receiveMessage(socket)
        KeyID = ad.messagesArray.pop(0).decode()
    else:
        KeyID = ad.messagesArray.pop(0).decode()
    if not KeyID.isnumeric():
        SERVER_SYNTAX_ERROR(socket)
    KeyID = int(KeyID)
    if KeyID > 4 or KeyID < 0:
        SERVER_KEY_OUT_OF_RANGE_ERROR(socket)
    return KeyID
