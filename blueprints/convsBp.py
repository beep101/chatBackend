from flask import Blueprint, request,g

from models import Conv,Participant ,iterableModelToJson
from sharedComponents import convsData, participantsData

convsBlueprint=Blueprint("conversations",__name__)

#GET
@convsBlueprint.route("/", methods=['GET'])
def getLastConvs():
    convs=[]
    if(g.user["admin"]):
        convs= convsData.getAllConvs()
    elif(g.user["admin"]==False):
        convs=convsData.getConvsByUserId(g.user["id"])
    else:
        return "Unauthorized", 401

    if(not convs):
        return "No conversations", 204
    json=iterableModelToJson(convs)
    return json

@convsBlueprint.route("/id/<int:id>", methods=['GET'])
def getConvById(id):
    conv= convsData.getConvById(id)
    if(not conv):
        return "No conversation", 204
    if(g.user["admin"]):
        return conv.toJson()
    for participant in conv.participants:
        if(participant.user==g.user["id"]):
            return conv.toJson()
    return "Unable to fetch resource", 404

#POST, PUT, DELETE
@convsBlueprint.route("/",methods=['POST'])
def addConv():

    newConv=Conv()
    newConv.fromJson(request.json)

    check=False
    for participant in newConv.participants:
        if(participant.user==g.user["id"]):
            check=True

    if(g.user["admin"] or check):
        insertedConv=convsData.addConv(newConv)

        if(insertedConv):
            participants=participantsData.addParticipantsToConv(insertedConv.id,newConv.participants)
            if(participants):
                insertedConv.participants=participantsData.getParticipantsForConv(insertedConv.id)
                return insertedConv.toJson()
            else:
                convsData.delConv(insertedConv)
                return "Bad request", 400
        else:
            return "Bad request",400
    else:
        return "Bad request",400

@convsBlueprint.route("/<int:id>",methods=['PUT'])
def modConv(id):
    changeConv=convsData.getConvById(id)
    if(not changeConv):
        return "No resource", 204
    changeConv.fromJson(request.json)
    changeConv.id=id

    if(g.user["admin"] or participantsData.getOneParticipantForConv(changeConv.id,g.user["id"])):
        conv=convsData.modConv(changeConv)
        if(conv):
            return conv.toJson()
        else:
            return "Bad request",400
    else:
        return "Bad request",400

@convsBlueprint.route("/<int:id>",methods=['DELETE'])
def delConv(id):
    conv=convsData.getConvById(id)
    if(conv):
        if(g.user["admin"]):
            result=participantsData.delParticipantsFromConv(conv.id)
            if(result):
                conv=convsData.getConvById(id)
                if(convsData.delConv(conv)):
                    return "Deleted conversation with ID = "+str(id)
                else:
                    return "Bad request", 400
            else:
                return "Bad request",400
        else:
            return "Unauthorized", 401
    else:
        return "Bad request",400

#*********************
#participant endpoints
#*********************

@convsBlueprint.route("/participant",methods=['POST'])
def addParticipant():

    print("adding")
    participant=Participant()
    participant.fromJson(request.json)

    if(g.user["admin"] or participantsData.getOneParticipantForConv(participant.conv,g.user["id"])):
        participant=participantsData.addParticipant(participant)
        if(participant):
            return participant.toJson()
        else:
            return "Bad request", 400
    else:
        return "Bad request", 400

@convsBlueprint.route("/participant/<int:convId>/<int:userId>",methods=['DELETE'])
def blockParticipant(convId,userId):

    if(g.user["admin"] or g.user["id"]==userId):
        participant=participantsData.getOneParticipantForConv(convId,userId)
        if(participant):
            participant.active=False
            if(participantsData.modParticipant(participant)):
                return "Success"
            else:
                return "Bad request",400
        else:
            return "Bad request",400        
    else:
        return "Unauthorized", 401




