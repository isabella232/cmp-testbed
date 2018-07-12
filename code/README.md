##Workflows

#workflow to extend existing driver 

just add methods which are warped by timing and tagging tags(resource consumption is optional)

#Workflow to add new driver 

In practice, drivers can be located anywhere in python project, but to keep things in order it is strongly recommended to place them under the corresponding folder like docker_based, docker_compose_based, library_based or website. An evaluation file of a driver should import Decorator class which is aimed to provide decorators for evaluation. Imported decorators should wrap the same as with extension of existing drivers methods which are added. The last step is to add the client to registered clients. It should be added to register.py file into the registered_cilents dictionary. The key name will be the name associated with the client in matrix.yml file and value the client itself.


##Data
Experements_data contains a raw data, where is a name of the folder corresponds to the name of the experiment and each file the combination of provider and action. Each row of the file contains information for every experiment. Each result has the following structure :

{"provider:item:action": {"consumption": {"start": {memory:{}, cpu{}}, "end": {memory:{}, cpu{}}, "time": 1111}}

