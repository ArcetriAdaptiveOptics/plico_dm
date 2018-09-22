import numpy as np
from plico.utils.decorator import override
from palpao.types.deformable_mirror_status import InstrumentStatus


__version__= "$Id: $"


class SimulatedDeformableMirrorClient(object):

    def __init__(self):
        self._actPos= np.zeros(2)
        self._commandCounter= 0


    @override
    def applyZonalCommand(self, actuatorPosition):
        self._actPos= actuatorPosition
        self._commandCounter+= 1


    @override
    def getZonalCommand(self):
        return self._actPos


    @override
    def offsetZonalCommand(self, actuatorOffset):
        self._actPos+= actuatorOffset
        self._commandCounter+= 1


    @override
    def applyModalCommand(self, actuatorPosition):
        self._actPos= actuatorPosition
        self._commandCounter+= 1


    @override
    def getModalCommand(self):
        return self._actPos


    @override
    def offsetModalCommand(self, actuatorOffset):
        self._actPos+= actuatorOffset
        self._commandCounter+= 1



    @override
    def getSnapshot(self):
        return {}


    @override
    def getStatus(self):
        return InstrumentStatus(
            self._actPos, self._commandCounter)

