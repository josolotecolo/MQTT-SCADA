# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 13:19:38 2014

@author: joso
"""

from collections import deque
import paho.mqtt.client as mqtt
import random
import proto_buf_schemas_pb2 as schemas


class descriptionModel:

    def __init__(self):
        self.protoDesc = schemas.description()

    # setters

    def setName(self, name):
        self.protoDesc.clientName = name

    def setDescription(self, desc):
        self.protoDesc.description = desc

    def addPoint(self, name, description):
        aux = self.protoDesc.points.add()
        aux.pointName = name
        aux.description = description

    def addAction(self, name, desc, args):
    # args must be a list of strings: ["string", "int", "float", etc...]
        aux = self.protoDesc.actions.add()
        aux.name = name
        aux.description = desc
        for a in args:
            aux2 = aux.arguments.add()
            aux2.name = a

    # getters

    def getClientName(self):
        return self.protoDesc.clientName()

    def getDescription(self):
        return self.protoDesc.description()

    def getPoints(self):  # returns a list of ("name", "description")
        aux = []
        for n in self.protoDesc.points:
            aux.append((n.pointName, n.description))
        return aux

    def getActions(self):
    # returns a list of ("name", "description", ["float", "int", etc...])
        aux = []
        for n in self.protoDesc.actions:
            aux2 = []
            for k in n.arguments:
                aux2.append(k)
            aux.append((n.name, n.description, aux2))
        return aux


class pointUpdateModel:

    def __init__(self):
        self.pointUpdate = schemas.pointUpdate()

    # setters

    def addValue(self, value):
        # allowed types: int, float, boolean, string
        self.pointUpdate.update = self.pointUpdate.updateType.add()
        if type(value) == int:
            self.pointUpdate.update.intResponse = value
        elif type(value) == float:
            self.pointUpdate.update.floatResponse = value
        elif type(value) == bool:
            self.pointUpdate.update.boolResponse = value
        elif type(value) == str:
            self.pointUpdate.update.strResponse = value

    # getters


class actionIssueModel:

    def __init__(self):
        self.actionQuer = schemas.actionQuery()

    # setters

    def setRemitent(self, rem):
        self.actionQuer.remitent = rem

    def setName(self, nam):
        self.actionQuer.name = nam

    def setId(self, iden):
        self.actionQuer.identifier = iden

    def setQos(self, qos):
        self.actionQuer.qos = qos

    def addArguments(self, args):
        # receives a list of args
        # allowed types: int, float, boolean, string
        for n in args:
            aux = self.actionQuer.arguments.add()
            if type(n) == str:
                aux.strVal = n
            elif type(n) == bool:
                aux.boolVal = n
            elif type(n) == int:
                aux.intVal = n
            elif type(n) == float:
                aux.floatVal = n

     # getters


class actionResponseModel:

    def __init__(self):
        self.actionResp = schemas.actionResponse()

    # setters

    def setIdentifier(self, iden):
        self.actionResp.identifier = iden

    def setError(self, desc):
        self.actionResp.errorDescription = desc

    def setResponse(self, val):
        aux = self.actionResp.response.add()
        if type(val) == str:
            aux.strResponse = val
        if type(val) == bool:
            aux.boolResponse = val
        if type(val) == int:
            aux.intResponse = val
        if type(val) == float:
            aux.floatResponse = val

    # getters


class inputBuffer:

    inputBufferDeq = deque()

    def insertMessage(payload):
        inputBuffer.inputBufferDeq.append(payload)

    def getMessage():
        if len(inputBuffer.inputBufferDeq) > 0:
            return inputBuffer.inputBufferDeq.popleft()


class outputBuffer:

    outputBufferDeq = deque()

    def insertMessage(payload):
        outputBuffer.outputBufferDeq.append(payload)

    def getMessage():
        if len(outputBuffer.outputBufferDeq) > 0:
            return outputBuffer.outputBufferDeq.popleft()


class actionsIssued:

    actionsBuffer = deque()

    def getAction():
        if len(actionsIssued.actionsBuffer) > 0:
            return actionsIssued.actionsBuffer.popleft()

    def insertAction(actionQuery):
        actionsIssued.actionsBuffer.append(actionQuery)


class parser:

    def serializeToString(schemaToString):
        return schemaToString.SerializeToString()

    def desToDescription(stringToSchema):
        aux = schemas.description()
        aux.ParseFromString(stringToSchema)
        return aux

    def desToActionQuery(stringToSchema):
        aux = schemas.actionQuery()
        aux.ParseFromString(stringToSchema)
        return aux

    def desToActionResponse(stringToSchema):
        aux = schemas.actionResponse()
        aux.ParseFromString(stringToSchema)
        return aux

    def desToPointUpdate(stringToSchema):
        aux = schemas.pointUpdate()
        aux.ParseFromString(stringToSchema)
        return aux

    def generalDeserialize(stringToSchema):  # returns a tuple (schema, type)
        try:
            aux = parser.desToPointUpdate(stringToSchema)
            return (aux, "pointUpdate")
        except:
            try:
                aux = parser.desToActionResponse(stringToSchema)
                return (aux, "actionResponse")
            except:
                try:
                    aux = parser.desToDescription(stringToSchema)
                    return (aux, "description")
                except:
                    try:
                        aux = parser.desToActionQuery(stringToSchema)
                        return (aux, "actionQuery")
                    except:
                        return None


class machine:

    def __init__(self):
        self.description = descriptionModel()
        self.actionsRegistered = {}  # {"action": action_method}

    # misc

    def machineActionDec():
        pass

    # processor thread

    # user interface

    def setMachineName(self, name):
        """
        Takes a string and sets the machine name.
        """
        if type(name) != str:
            return None
        self.description.setName(name)

    def addPointToDescription(self, name, desc):
        """
        Takes a point name and a description (strings) and adds the point
        to the description.
        """
        if (type(name) != str) or (type(desc) != str):
            return None
        self.description.addPoint(name, desc)

    def addActionToDescription(self, name, desc, args, func):
        """
        Takes a str as name, a str as description and a list of str specifying
        each argument type, ej: ["float", "int", "str", "float"]
        """
        if (type(name) != str) or (type(desc) != str):
            return None
        for n in args:
            if type(n) != str:
                return None
        self.description.addAction(name, desc, args)


class mqttClient:

    def __init__(self, **kwargs):

        self.clientId = kwargs["clientId"]
        self.userName = kwargs["userName"]
        self.password = kwargs["password"]
        self. certAuth = kwargs["certAuth"]
        self.host = kwargs["host"]
        self.port = kwargs["port"]
        self.keepalive = kwargs["keepalive"]
        self.protocol = kwargs["protocol"]
        self.maxInflightMessages = kwargs["maxInflightMessages"]
        self.messageRetryTime = kwargs["messageRetryTime"]
        self.rootTopic = kwargs["rootTopic"]
        self.pahoClient = mqtt(client_id=self.clientId,
                               clean_session=True,
                               protocol="MQTTv31",
                               userdata=None)
        self.pahoCLient.max_inflight_messages_set(self.maxInflightMessages)
        self.pahoClient.message_retry_set(self.messageRetryTime)
        self.pahoClient.username_pw_set(username=self.userName,
                                        password=self.password)

        # register callbacks

        self.pahoClient.on_connect = mqttClient.on_connect
        self.pahoClient.on_message = mqttClient.on_message
        self.pahoClient.on_disconnect = mqttClient.on_disconnect
        self.pahoClient.on_unsubscribe = mqttClient.on_unsubscribe
        self.pahoClient.on_subscribe = mqttClient.on_subscribe
        self.pahoClient.on_publish = mqttClient.on_publish

        # misc

        self.machineBroadcast = self.rootTopic + "BROADCAST/MACHINES"
        self.operatorBroadcast = self.rootTopic + "BROADCAST/OPERATORS"
        self.connectionStatus = False
        self.publishSuc = deque()
        self.subscribeSuc = deque()
        self.unsubscribeSuc = deque()

    def on_connect(client, userdata, flags, rc):
        client.connectionStatus = True

    def on_message(client, userdata, message):
        inputBuffer.insertMessage(message.payload)

    def on_publish(client, userdata, mid):
        client.publishSuc.append(mid)

    def on_disconnect(client, userdata, rc):
        client.connectionStatus = False

    def on_unsubscribe(client, userdata, mid):
        client.unsubscribeSuc.append(mid)

    def on_subscribe(client, userdata, mid, granted_qos):
        client.subscribeSuc.append(mid)

    def powerUp(self):
        # if this method returns false, better to
        # reinstantiate the whole mqttClient class
        self.pahoClient.connect_async(self.host, self.port, self.keepalive)
        try:
            self.pahoClient.loop_start()
        except:
            return False
        else:
            return True

    def cleanShutDown(self):
        if self.connectionStatus:
            self.pahoClient.disconnect()
        while self.connectionStatus:
            pass
        self.pahoClient.loop_stop()
        return True

    def publish(self, destination, toPublish, qos):
        aux = self.pahoClient.publish(destination, qos=qos,
                                      payload=toPublish)
        if aux[0] == "MQTT_ERR_NO_CONN":
            return None
        return aux[1]

    def subscribe(self, topic, qos):
        aux = self.pahoClient.subscribe(topic, qos)
        if aux[0] == "MQTT_ERR_NO_CONN":
            return None
        return aux[1]

    def unsubscribe(self, topic):
        aux = self.pahoClient.unsubscribe(topic)
        if aux[0] == "MQTT_ERR_NO_CONN":
            return None
        return aux[1]

    def returnStats(self):
        aux = {"p": [], "s": [], "u": []}
        while len(self.publishSuc) > 0:
            aux["p"].append(self.publishSuc.popleft())
        while len(self.subscribeSuc) > 0:
            aux["s"].append(self.subscribeSuc.popleft())
        while len(self.unsubscribeSuc) > 0:
            aux["u"].append(self.unsubscribeSuc.popleft())
        return aux

    def getClientArgs(clientId=False, userName="genericUser",
                      password="genericPassword", certAuth=False,
                      host="127.0.0.1", port=1883, keepalive=60,
                      protocol="MQTTv31", maxInflightMessages=20,
                      messageRetryTime=5, rootTopic="MQTTSCADA/"):
        clientArgs = {}
        if not clientId:
            clientArgs.update({"clientId": random.randint(1, 10000)})
        else:
            clientArgs.update({"clientId": str(clientId)})
        clientArgs.update({"userName": str(userName)})
        clientArgs.update({"password": str(password)})
        clientArgs.update({"certAuth": str(certAuth)})
        clientArgs.update({"host": str(host)})
        clientArgs.update({"port": int(port)})
        clientArgs.update({"keepalive": int(keepalive)})
        clientArgs.update({"protocol": str(protocol)})
        clientArgs.update(
            {"maxInflightMessages": int(maxInflightMessages)})
        clientArgs.update({"messageRetryTime": int(messageRetryTime)})
        clientArgs.update({"rootTopic": str(rootTopic)})
        return clientArgs
