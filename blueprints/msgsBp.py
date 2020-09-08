from flask import Blueprint, request, g
import json
import decimal

from sharedComponents import msgsData, msgsService, participantsData

msgsBlueprint=Blueprint("messages",__name__)

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

@msgsBlueprint.route("/",methods=['POST'])
def addMsg():
    if(msgsService.addMessage(request.json,None)):
        return "Success"
    else:
        return "Error", 400

@msgsBlueprint.route("/<int:convId>",methods=['GET'])
def getMsgs(convId):
    participant=isParticipant(convId)
    if(participant):
        last=participant.recieved
        results=msgsData.getMsgsTo(convId,last)
        if(results):
            participant.recieved=results[0]['msgNum']
            participantsData.modParticipant(participant)
        return json.dumps(results, default=decimal_default)
    else:
        return "Uauthorized to access ", 401

@msgsBlueprint.route("/<int:convId>/<int:count>",methods=['GET'])
def getCountedMsgs(convId,count):
    if(isParticipant(convId)):
         return json.dumps(msgsData.getMsgsCount(convId,count), default=decimal_default)
    else:
        return "Unauthorized to access", 401

@msgsBlueprint.route("/<int:convId>/<int:fromMsg>/<int:count>",methods=['GET'])
def getCountedMsgsFrom(convId,fromMsg,count):
    if(isParticipant(convId)):
         return json.dumps(msgsData.getMsgsFromCount(convId,fromMsg,count), default=decimal_default)
    else:
        return "Unauthorized to access",401

def isParticipant(convId):
    return participantsData.getOneParticipantForConv(convId,g.user["id"])
    

