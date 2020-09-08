from dataAccess.usersData import UsersData
from dataAccess.convsData import ConvsData
from dataAccess.participantsData import ParticipantsData
from dataAccess.msgsData import MsgsData
from services.authService import AuthService
from services.msgsService import MessagingService

usersData=UsersData()
participantsData=ParticipantsData()
convsData=ConvsData()
msgsData=MsgsData()

authService=AuthService(usersData)
msgsService=MessagingService(convsData,msgsData)