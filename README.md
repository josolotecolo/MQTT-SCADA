MQTT-SCADA
==========
A SCADA framework for MQTT protocol.

<h3>Objective:</h3>
Create a framework that enables the user to create SCADA systems on top of the MQTT protocol on a relative easy way.

<h3>Draft:</h3>
The system is conformed of two types of actors. The masters and the slaves. However, since slavery was abolished long ago (supposedly), i will use names more accordingly to the project context: operators and machines, respectively. <br>
<ul>
<li>Machines: A machine is an actor capable of executing actions that an operator issues and is also capable of give information about its state points. For example, a motor can be a machine with the following points: rotor speed and temperature. Some actions that could be executed on that motor are: control speed, control temperature, turn off, turn on, etc...
<li>Operators: The operator is the actor responsible for reading the machines points and executing actions on them. Following the above example, the operator of the motor can be a person reading the speedometer and thermometer and capable of turning switches and buttons in order to control speed, temperature and state of the motor.
</ul> <br>
The following image describes the relations between machines and operators on an MQTT protocol context.

