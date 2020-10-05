import boto3
from botocore.config import Config
from boto3.dynamodb.conditions import Key
import datetime

import config


class MsgsData:
    def __init__(self):
        self.dynamo = boto3.resource('dynamodb',region_name = config.region_name, aws_access_key_id=config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)
        self.table=self.dynamo.Table('messagesChatApp')

    def getMsgsTo(self,convId,msgId):
        response=self.table.query(KeyConditionExpression=Key('conversation').eq(convId) & Key('msgNum').gt(msgId),ScanIndexForward=False)
        return response['Items']

    def getMsgsCount(self, convId, count):
        response=self.table.query(KeyConditionExpression=Key('conversation').eq(convId),Limit=count,ScanIndexForward=False)
        return response['Items']

    def getMsgsFromCount(self, convId, msgId, count):
        response=self.table.query(KeyConditionExpression=Key('conversation').eq(convId) & Key('msgNum').lte(msgId),Limit=count,ScanIndexForward=False)
        return response['Items']

    def addMsg(self, convId, userId,msgText):
        msgNum=int(datetime.datetime.now().timestamp() * 1000)
        self.table.put_item(
            Item={
            'conversation':convId,
            'msgNum':msgNum,
            'user':userId,
            'msg':msgText
        })
        return msgNum

    def modMsg(self, convId, msgId, msgText):
        pass

    def delMsg(self, convId, msgId):
        pass
