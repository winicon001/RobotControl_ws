This is a package intended for serial communication from a Linux dev machine running a publisher node to an 
arduino/raspberry robot needing central command. It is intended to be used for multiple robots. 

The publisher node advertises the input to the terminal over the topic and every node runnning the 
corresponding subscriber node, suibscribed to the topic gets the command and use the string received accordingly.

This is a simple implementation of arduino serial commuunication. It can be expanded besed on use case

Please get in touch if you see an opportunity to make it better.
