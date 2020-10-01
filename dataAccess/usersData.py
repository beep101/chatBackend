from database import makeSession
from models import User

class UsersData:
    
    def getAllUsers(self):
        session=makeSession()
        allUsers=session.query(User).all()
        session.close()
        return allUsers

    def getAllUsersNoAdmin(self):
        session=makeSession()
        allUsers=session.query(User).filter(User.admin==False).all()
        session.close()
        return allUsers


    def getUserById(self,id):
        session=makeSession()
        user=session.query(User).filter(User.id==id).first()
        session.close()
        return user

    def getUserByEmail(self,email):
        session=makeSession()
        users=session.query(User).filter(User.email==email).first()
        session.close()
        return users

    def findUserByName(self,name):
        session=makeSession()
        user=session.query(User).filter(User.name.like('%'+name+'%')).all()
        session.close()
        return user
    
    def findUserByNameNoAdmin(self,name):
        session=makeSession()
        user=session.query(User).filter(User.name.like('%'+name+'%')).filter(User.admin==False).all()
        session.close()
        return user

    def addUser(self,user):
        session=makeSession()
        session.add(user)
        session.flush()
        session.refresh(user)
        check=True
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.refresh(user)
            session.close()
            if(check):
                return user
            else:
                return None
    
    def modUser(self,user):
        session=makeSession()
        crrUser=session.query(User).filter(User.id==user.id).first()
        check=True
        if(crrUser):
            crrUser.name=user.name
            crrUser.email=user.email
            crrUser.admin=user.admin
            crrUser.passwd=user.passwd
        else:
            check=False
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.refresh(crrUser)
            session.close()
            if(check):
                return crrUser
            else:
                return None

    def delUser(self,user):
        session=makeSession()
        session.delete(user)
        check=True
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.close()
            if(check):
                return True
            else:
                return None


