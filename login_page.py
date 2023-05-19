from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('login_page'))


@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = session.get('room')
    join_room(room)
    message = f"{username} has joined the {room} room."
    emit('status', {'msg': message}, room=room)


@socketio.on('leave')
def on_leave(data):
    username = session.get('username')
    room = session.get('room')
    leave_room(room)
    message = f"{username} has left the {room} room."
    emit('status', {'msg': message}, room=room)


@socketio.on('send_message')
def handle_send_message(data):
    username = session.get('username')
    room = session.get('room')
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
    message = {'username': username, 'msg': data['msg'], 'timestamp': timestamp}
    emit('receive_message', message, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
