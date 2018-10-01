


class DeformableMirrorStatus(object):

    def __init__(self,
                 numberOfActuators,
                 numberOfModes,
                 actuatorCommands,
                 commandCounter):
        self._numberOfActuators= numberOfActuators
        self._numberOfModes= numberOfModes
        self._actuatorCommands= actuatorCommands
        self._commandCounter= commandCounter


    def commandCounter(self):
        return self._commandCounter


    def actuatorCommands(self):
        return self._actuatorCommands


    def numberOfActuators(self):
        return self._numberOfActuators


    def numberOfModes(self):
        return self._numberOfModes
