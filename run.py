from flask import Flask, render_template,request
from flask_socketio import SocketIO, join_room, emit
import random
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)

connectedClients = []
secure_random = random.SystemRandom()

roomList = ['general','tech']

@app.route("/")
def index():
    if request.remote_addr in connectedClients:
        return render_template('index.html')
    else:
        return render_template('login.html')
        
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        pass
        return redirect("http://localhost:5000/login", code=302)
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
            pass
        else:
            error = 'Invalid Credentials. Please try again.'
        return redirect("http://localhost:5000/", code=302)
    return render_template('login.html', error=error)
