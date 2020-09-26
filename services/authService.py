import string
import hashlib
import random
import binascii
import jwt

class AuthService:
    secretKey='testtesttest'    
    users=[]

    def __init__(self,usersData):
        self.usersData=usersData

    def createJwt(self,user):
        return self.__encodeJwt(user)

    def checkJwt(self,token):
        data=self.__decodeJwt(token)
        if(not data):
            return None
        check=self.__checkUser(data["id"])
        return check 

    def hashPassword(self,password):
        lets=string.ascii_letters
        salt = ''.join(random.choice(lets) for i in range(16))
        digest=self.__hash(password,salt)
        return salt+digest

    def checkPassword(self,salthash,password):
        salt=salthash[:16]
        savedPassword=salthash[16:]
        providedPassword=self.__hash(password,salt)
        if(savedPassword==providedPassword):
            return True
        else :
            return False

    def __hash(self,password,salt):
        digest=hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),salt.encode('ascii'),100000)
        digest = binascii.hexlify(digest)
        return digest.decode('ascii')

    def __encodeJwt(self,user):
        return jwt.encode({'id':user.id,'email':user.email,'name':user.name,'amdin':user.admin},self.secretKey,algorithm='HS256')

    def __decodeJwt(self,token):
        try:
            decoded=jwt.decode(token,self.secretKey,algorithm='HS256')
            return decoded
        except Exception:
            return None
    
    def __loadUser(self,id):
        user=self.usersData.getUserById(id)
        userDict={"id": user.id,"admin":user.admin}
        self.users.append(userDict)
        return userDict

    def __checkUser(self,id):
        for user in self.users:
            if(user["id"]==id):
                return user
        user=self.__loadUser(id)
        if(user["id"]==id):
            return user
        return None