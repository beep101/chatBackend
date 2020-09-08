from flask import g
from flask_socketio import emit

class MessagingService:
    userBySession={}
    sessionByUser={}
    #from app import socketio

    def __init__(self,convsData,msgsData):
        self.convsData=convsData
        self.msgsData=msgsData

    def addMessage(self,request,sesssionId):
        if(sesssionId):
            userId=self.userBySession[sesssionId]
        else:
            userId=g.user["id"]
        conv= self.convsData.getConvById(int(request['convId']))

        for participant in conv.participants:
            if(participant.user==userId):
                self.msgsData.addMsg(int(request['convId']),userId,request['message'])
                self.__notifyMessage(conv.participants,{'convId':int(request['convId']),'userId':userId,'message':request['message']})
                return True
        return False

    def __notifyMessage(self,participants,message):
        for participant in participants:
            emit('message',message,room=self.sessionByUser[participant.user])

    def addUser(self,userId,sessionId):
        self.userBySession[sessionId]=userId
        self.sessionByUser[userId]=sessionId 

    def removeUser(self,sessionId):
        userid=self.userBySession.get(sessionId)
        if(userid):
            self.userBySession.pop(userid)
            self.sessionByUser.pop(sessionId)
            #********************
            #record last recieved
            # *******************    
