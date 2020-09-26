from database import makeSession
from models import Conv,Participant
from sqlalchemy.orm import joinedload


class ConvsData:

    def getAllConvs(self):
        session=makeSession()
        res=session.query(Conv).options(joinedload(Conv.participants).joinedload(Participant.userObj)).all()
        session.close()
        return res

    def getConvById(self,id):
        session=makeSession()
        res=session.query(Conv).options(joinedload(Conv.participants).joinedload(Participant.userObj)).filter(Conv.id==id).first()
        session.close()
        return res

    def getConvsByUserId(self,id):
        session=makeSession()
        res=session.query(Conv).join(Conv.participants).filter(Participant.user==id).join(Participant.userObj).all()
        session.close()
        return res

    def addConv(self,conv):
        session=makeSession()
        session.add(conv)
        session.flush()
        session.refresh(conv)
        check=True
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.refresh(conv)
            session.close()
            if(check):
                return conv
            else:
                return None

    def modConv(self,conv):
        session=makeSession()
        crrConv=session.query(Conv).filter(Conv.id==conv.id).first()
        check=True
        if(crrConv):
            crrConv.name=conv.name
            crrConv.msgs=conv.msgs
        else:
            check=False
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.refresh(crrConv)
            session.close()
            if(check):
                return crrConv
            else:
                return None

    def delConv(self,conv):
        session=makeSession()
        session.delete(conv)
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