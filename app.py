from flask import Flask, request, g
from flask_socketio import SocketIO, emit

from sharedComponents import authService, msgsService
from config import SECRET_KEY

app=Flask("chapp")

app.config['SECRET_KEY'] = SECRET_KEY
socketio=SocketIO(app, cors_allowed_origins="*")


from blueprints.usersBp import usersBlueprint
from blueprints.convsBp import convsBlueprint
from blueprints.msgsBp import msgsBlueprint
from blueprints.authBp import authBlueprint


app.register_blueprint(usersBlueprint, url_prefix='/users')
app.register_blueprint(convsBlueprint, url_prefix='/convs')
app.register_blueprint(msgsBlueprint, url_prefix='/msgs')
app.register_blueprint(authBlueprint)

@app.before_request
def before_request():
    if request.path !="/login" and request.path !="/signup":
        if(not request.headers.get('Authorization')):
            return "Unauthorized", 401
        g.user=authService.checkJwt(request.headers['Authorization'][7:])

@socketio.on('connect', namespace='/msgs')
def connectUser():
    emit('connected')

@socketio.on('authorize', namespace='/msgs')
def authorizeUser(requestJson):
    user=authService.checkJwt(requestJson["token"])
    if(user):
        msgsService.addUser(user["id"],request.sid)
        emit("authorized",{'data':'valid token'})
    else:
        emit("authorized",{'data':'invalid token'})
    

@socketio.on('disconnect', namespace='/msgs')
def disconnectUser():
    msgsService.removeUser(request.sid)

@socketio.on('message', namespace='/msgs')
def recieveMsg(requestJson):
    msgsService.addMessage(requestJson,request.sid)
    

if __name__ == '__main__':
    socketio.run(app,debug=True)