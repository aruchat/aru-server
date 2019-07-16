from flask import Flask, render_template,request
from flask_socketio import SocketIO, join_room, emit
import random
import json
from flask_cors import CORS

# proof of concept
# Slack Crow(Aru team) 2018-2019

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)

keySet = dict()
connectedClients = []
secure_random = random.SystemRandom()
keyOwner = ""
serverWideKeySet = False

roomList = ['general','meme']

@app.route("/")
def index():
    return render_template('index.html')


@socketio.on('send')
def sub(data):
    data['sender'] = request.sid 
    print(data)
    emit('sendMsg', json.dumps(data),broadcast=True)

@socketio.on('getKey')
def getKey(data):
    print('getKey')
    print(data)
    global keySet
    keySet[request.sid] = data['publicKey']
    toSend = dict()
    toSend['key'] = data['publicKey']
    toSend['cid'] = request.sid
    emit('giveRoomKeyNow', json.dumps(toSend), room=keyOwner)

@socketio.on('getRoomKey')
def getRoomKey(data):
    print('getRoomKey')
    print(data)
    emit('setRoomKeyNow', data['encryptedKey'], room=data['sid'])

@socketio.on('keySet')
def setKeyConfirmed(data):
    global keyOwner
    global serverWideKeySet
    keyOwner = request.sid
    print('Key set')
    print('Key Owner: ' + keyOwner)
    serverWideKeySet = True
    for client in connectedClients:
        if len(connectedClients) == 1:
            break
        elif client == keyOwner:
            continue
        else:
            print('test')
            emit('givePubKeyNow', "", room=client)


@socketio.on('connect')
def handle_connect():
    global connectedClients
    connectedClients.append(request.sid)
    print('Client connected')
    if not serverWideKeySet:
        emit('setKeyNow', "", room=request.sid)
    else:
        emit('givePubKeyNow', "", room=request.sid)
    for client in connectedClients:
        print(connectedClients)
        emit('userListUpdate', json.dumps(connectedClients), room=client)
        
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    global connectedClients
    global keyOwner
    global serverWideKeySet
    connectedClients.remove(request.sid)
    if request.sid == keyOwner:
        print('(ERR) Key holder disconnected')
        if len(connectedClients) != 0:
            clientToSetKey = secure_random.choice(connectedClients)
            emit('setKeyNow', "", room=clientToSetKey)
        else:
            serverWideKeySet = False
    for client in connectedClients:
        emit('userListUpdate', json.dumps(connectedClients), room=client)

if __name__ == '__main__':
    socketio.run(app)
