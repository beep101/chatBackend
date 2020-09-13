from flask import Blueprint, request,g

from models import User,iterableModelToJson
from sharedComponents import usersData

usersBlueprint = Blueprint("users",__name__)

#GET
@usersBlueprint.route("/", methods=['GET'])
def getUsers():
    users=usersData.getAllUsers()
    json=iterableModelToJson(users)
    return json

@usersBlueprint.route("/all", methods=['GET'])
def getAllUsers():
    users=usersData.getAllUsers()
    json=iterableModelToJson(users)
    return json

@usersBlueprint.route("/id/<int:id>", methods=['GET'])
def getUserById(id):
    user=usersData.getUserById(id)
    if(user):
       return user.toJson()
    else:
        return "Bad request", 400

@usersBlueprint.route("/find/<term>", methods=['GET'])
def findUserByName(term):
    users=usersData.findUserByName(term)
    json=iterableModelToJson(users)
    return json

#POST, PUT, DELETE
@usersBlueprint.route("/",methods=['POST'])
def addUser():
    if(g.user["admin"]):
        request.json["passwd"]=passwd=authService.hashPassword(request.json["passwd"])
        newUser=User()
        newUser.fromJson(request.json)
        newUser=usersData.addUser(newUser)
        if(newUser):
            return newUser.toJson(), 201
        else:
            return "Bad request",400
    else:
        return "Unauthorized", 401

@usersBlueprint.route("/<int:id>",methods=['PUT'])
def modUser(id):
    if(g.user["admin"] or g.user["id"]==id):
        if("passwd" in request.json):
            request.json["passwd"]=authService.hashPassword(request.json["passwd"])
        changeUser=usersData.getUserById(id)
        if(not changeUser):
            return "No resource", 204
        changeUser.fromJson(request.json)
        changeUser.id=id
        changeUser=usersData.modUser(changeUser)
        print(changeUser)
        if(changeUser):
            return changeUser.toJson()
        else:
            return "Bad request", 400
    else:
        return "Unauthorized", 401

@usersBlueprint.route("/<int:id>",methods=['DELETE'])
def delUser(id):
    if(g.user["admin"]):
        deleteUser=usersData.getUserById(id)
        if(not deleteUser):
            return "Bad request", 400
        if(usersData.delUser(deleteUser)):
            return "Deleted user with ID = "+str(id)
        else:
            return "Bad request", 400
    else:
        return "Unauthorized",401