from database import makeSession
from models import Participant
from sqlalchemy.orm import joinedload

class ParticipantsData:
    def getParticipantsForConv(self,convId):
        session=makeSession()
        participantsInConversation=session.query(Participant).options(joinedload(Participant.userObj)).filter(Participant.conv==convId).all()
        session.close()
        return participantsInConversation

    def getOneParticipantForConv(self,convId,userId):
        session=makeSession()
        participant=session.query(Participant).options(joinedload(Participant.userObj)).filter(Participant.user==userId).filter(Participant.conv==convId).first()
        session.close()
        return participant

    def addParticipant(self,participant):
        session=makeSession()
        session.add(participant)
        check=True
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.refresh(participant)
            session.close()
            if(check):
                return participant
            else:
                return None

    def modParticipant(self,participant):
        session=makeSession()
        crrParticipant=session.query(Participant).filter(Participant.user==participant.user).filter(Participant.conv==participant.conv).first()
        if(not crrParticipant):
            return False
        check=True
        if(crrParticipant):
            crrParticipant.recieved=participant.recieved
            crrParticipant.seen=participant.seen
            crrParticipant.active=participant.active
        else:
            check=False
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            session.refresh(crrParticipant)
            session.close()
            if(check):
                return crrParticipant
            else:
                return None

    def delParticipant(self,participant):
        session=makeSession()
        session.delete(participant)
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


    #**************************
    #additional functionalities
    #**************************
    def delParticipantsFromConv(self,convId):
        session=makeSession()
        participants=session.query(Participant).filter(Participant.conv==convId).all()
        for participant in participants:
            session.delete(participant)
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

    def addParticipantsToConv(self,convId,participants):
        session=makeSession()
        for participant in participants:
            session.add(participant)
        check=True
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            check=False
        finally:
            for participant in participants:
                session.refresh(participant)
            session.close()
            if(check):
                return participants
            else:
                return None