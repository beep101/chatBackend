from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    email=Column(String(100))
    passwd=Column(String(80))
    name=Column(String(100))
    admin=Column(Boolean,default=False)

    def toJson(self):
        json='{'
        json=json+'"id":'+str(self.id)+','
        json=json+'"email":"'+self.email+'",'
        #json=json+'"passwd":"'+self.passwd+'",'
        json=json+'"name":"'+self.name+'",'
        json=json+'"admin":"'+str(self.admin)+'"'
        json=json+"}"
        return json

    def fromJson(self,data):
        if("id" in data):
            self.id=int(data["id"])
        if("email" in data):
            self.email=data["email"]
        if("passwd" in data):
            self.passwd=data["passwd"]
        if("name" in data):
            self.name=data["name"]
        if("admin" in data):
            self.admin=data["admin"]=="True"

class Participant(Base):
    __tablename__="userConv"
    recieved=Column(Integer,default=0)
    seen=Column(Integer,default=0)
    active=Column(Boolean,default=True)
    conv=Column(Integer,ForeignKey('conversations.id'),primary_key=True)
    user = Column(Integer, ForeignKey('users.id'),primary_key=True)
    convObj=relationship("Conv",lazy="joined")
    userObj=relationship("User",lazy="joined")

    def toJson(self):
        json="{"
        json=json+'"user":'+str(self.user)+","
        json=json+'"conv":'+str(self.conv)+","
        json=json+'"recieved":'+str(self.recieved)+","
        json=json+'"seen":'+str(self.seen)+","
        json=json+'"active":"'+str(self.active)+'",'
        json=json+'"userObj":'+self.userObj.toJson()
        json=json+"}"
        return json

    def fromJson(self,data):
        if("conv" in data):
            self.conv=int(data["conv"])
        if("user" in data):
            self.user=int(data["user"])
        if("active" in data):
            self.active=data["active"]=="True"
        if("recieved" in data):
            self.recieved=int(data["recieved"])
        if("seen" in data):
            self.seen=int(data["seen"])


class Conv(Base):
    __tablename__='conversations'
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50))
    msgs=Column(Integer,default=0)
    participants = relationship("Participant",back_populates="convObj",lazy="joined")

    def toJson(self):
        json="{"
        json=json+'"id":'+str(self.id)+','
        if(self.name):
            json=json+'"name":"'+self.name+'",'
        else:
            json=json+'"name":"",'
        json=json+'"msgs":'+str(self.msgs)+','
        json=json+'"participants":'+iterableModelToJson(self.participants)
        json=json+"}"
        return json

    def fromJson(self,data):
        if("id" in data):
            self.id=int(data["id"])
        if("name" in data):
            self.name=data["name"]
        if("msgs" in data):
            self.msgs=int(data["msgs"])
        self.participants=[]
        if("participants" in data):
            for participantData in data["participants"]:
                participant=Participant()
                participant.fromJson(participantData)
                self.participants.append(participant)

def iterableModelToJson(iterable):
    json='[ '
    for element in iterable:
        json=json+element.toJson()+','
    json=json[:-1]+' ]'
    return json

