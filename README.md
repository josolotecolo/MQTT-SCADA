MQTT-SCADA
==========
A SCADA framework for MQTT protocol.

<h2>Objective:</h2>
Create a framework/application_layer that enables the user to create SCADA systems on top of the MQTT protocol on a relative easy way.

<h2>Draft:</h2>
The system is conformed of two types of actors. The masters and the slaves. However, since slavery was abolished long ago (supposedly), i will use names more accordingly to the project's context: operators and machines, respectively. <br>
<ul>
<li>Machines: A machine is an actor capable of executing actions that an operator issues and is also capable of give information about its state points. For example, a motor can be a machine with the following points: rotor speed and temperature. Some actions that could be executed on that motor are: control speed, control temperature, turn off, turn on, etc...
<li>Operators: The operator is the actor responsible for reading the machines points and executing actions on them. Following the above example, the operator of the motor can be a person reading the speedometer and thermometer and capable of turning switches and buttons in order to control speed, temperature and state of the motor.
</ul>
<h3>Operation</h3>
The principle of operation of the system is simple: Each machine should implement a machine's description. Here are described all the action that the machine can execute and all the points available for it. Operators should be aware of machines descriptions in order to know wich actions can be issued or wich points can be read. <br>
When an operator issues an action to a machine, the machine executes the action requested and can return a value to the operator.  <br>
Operators can also listen to machine points without the need of issuing any action. <br>
In order to bring this to the MQTT protocol context, I made the following schema, where the relations that must exist between a machine called 'Machine_1' and an operator called 'Operator_1' are shown:
<p align="center">
<img src="https://cloud.githubusercontent.com/assets/9935348/5175413/1c7dc21c-7400-11e4-8fe3-635df8b5030a.png" height=500 width=500>
</p>
<ul>
<li>The MQTTSCADA/BROADCAST/MACHINES MQTT topic: An operator publishes an action to this topic when it wants all the machines of the network to perform the same action. <br>
Discovery: Discovery is when an operator retrieves machines descriptions. In order to perform discovery by means of an operator broadcasting an action, machines must have an action called getDescription that returns its description and must be subscribed to this topic. However, it is not mandatory that all machines implement this action and subscribe to this topic because an operator can get to know a machine's name and description by other means. <br>
The QoS for subscribing to this topic can be a configuration property of the machine, but, since a lot of machines will be subsribed to this topic it is recommended a QoS of 0, however, this could lead to machines not being discovered by operators. The use of QoS 1 means that the getDescription issue can arrive more than one time. This means that there will be multiple responses, a very bad scenario, so if the QoS needs to be raised, it must be a QoS = 2. For the publishing QoS of the operator, it must be 0 or 2, since a QoS = 1 will present the same problems described before.
<li>MQTTSCADA/POINTS/Machine_1/P1 ... Pn topics: P1, P2, ... Pn correspond to machine's point names. Machine publish the data of its points in these topics. Operators can subscribe to the topics that are interested in. The QoS for publishing or subscribing for machine points can be 0, 1, or 2 since problems related from selection QoS = 1 are less significant in this case.
<li>MQTTSCADA/ACTIONINPUT/Machine_1 topic: Each machine should be subscribed to this topic where operators can issue actions by publishing on it. Machines that don't implement actions may ommit this topic. Publishing asnd subscribing to this topic must be done with QoS = 0 or QoS = 2.
<li>MQTTSCADA/ACTIONRESPONSE/Operator_1 topic: If the operator is able to issue actions, it must be subscribed to this topic in order to receive the posible action responses from the machines. Publishing asnd subscribing to this topic must be done with QoS = 0 or QoS = 2.
<li>MQTTSCADA/BROADCAST/OPERATORS topic: Issuing the getDescription action for machine discovery could lead to unnecessary transactions and network congestion since every machine will respond almost at the same time with their descriptions, so, it must be used with care. Another mecanism for machine discovery could be sending the machine's description to this topic when it is started. Operators that are subscribed to this topic receive the description of the new machine and become aware of it. Of course, this discovery mechanism could be not good for the network too if the number of operators is relatively high. While the receiving of a description can mean that a machine is online, the detection of a disconnected machine can be done through the will characteristic of the MQTT protocol. So, the associated clients of machines can be configured to set a will on this topic. When a machine disconnects, voluntary or involuntary, the broker will publish the disconnection message on this topic. <br>
Publishing and subscribing to this topic can be done with QoS = 0, 1 or 2.
</ul>
<h3>Message types</h3>
According to what has been said above, five types of messages can be identified:
<ul>
<li>Descriptions: The description of a machine holds a general description of what the machine does; the actions that can be issued to it and a description of each one including the parameters that can be passed; and the points that it publishes and a description of each one. It must also hold the machine name since descriptions could arrive to operators via broadcasting, where there is no reference to the machine that sended the description. 
<li>Disconnection message: When a machine is disconnected from the MQTT broker, this will broadcast the disconnection message to the operators subscribed to MQTTSCADA/BROADCAST/OPERATORS. This message must include the machine name that was disconnected.
<li>Action issue: A message of an action issue must contain the action to be executed and the parameters of that action (if any). Because the action can return information to the operator that issued it, it is convenient to include an integer number as identifier in order for the operator to differentiate the actions that it issues. <br>
Since the actions are published on MQTTSCADA/ACTIONINPUT/Machine_x topic, there is no reference to the operator that issued the action, so,  the action issue must contain the name of the operator that issued the action.
<li>Action response: The action response must contain the result of the action that the machine executed, the error message if the action could not be executed and an identifier. The identifier must be the same number that the operator sended on the action issue that triggered the response. This identifier could be sufficient in order to determine the machine's name that sended the response. Nevertheless, it may be better to add the machine name on the response.
<li>Point update from the machine: A point update occurs when a machine updates the value of one of its points by publishing it to the broker. There is no need for more information other than the value of the point since the topic in which points are published include the name of the machine. Also, in the description of the point must be specified the type of the value.
</ul>
<h3>MQTT client considerations</h3>
Every machine and operator is associated with an MQTT client and should be configured according to the following points in order to mantain the broker clean.
<ul>
<li>The MQTT client id should be the machine / operator name. 
<li>All clients should connect with the clean session flag set to True.
<li>All clients should publish with retain set to False.
</ul>

