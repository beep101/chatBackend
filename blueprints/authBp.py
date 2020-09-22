from flask import Blueprint, request

from models import User
from sharedComponents import authService, usersData

authBlueprint=Blueprint("auth",__name__)

@authBlueprint.route("/login",methods=['POST'])
def login():
    
    user=usersData.getUserByEmail(request.json['email'])
    if(user == None):
        return 'Pogresan email', 401
    if(authService.checkPassword(user.passwd,request.json['passwd'])):
        return authService.createJwt(user)
    else:
        return 'Pogresan password', 401

@authBlueprint.route("/signup",methods=['POST'])
def signup():
    password=authService.hashPassword(request.json['passwd'])
    user=User( email=request.json['email'],passwd=password,name=request.json['name'],admin=False)
    check=usersData.addUser(user)
    if(check):
        return "Kreiran korsinik", 201
    else:
        return "Greska", 400

@authBlueprint.route("/check",methods=['GET'])
def check():
    return "Authorized"
