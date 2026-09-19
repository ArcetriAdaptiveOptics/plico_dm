import abc
import numpy as np
from plico.utils.decorator import returnsNone, returns, returnsForExample
from plico_dm.types.modulator_status import ModulatorStatus
from six import with_metaclass


class SnapshotEntry(object):
    MODULATOR_AMPLITUDE = "MODULATOR_AMPL"
    MODULATOR_FREQUENCY = "MODULATOR_FREQ"
    MODULATOR_CENTER_AXIS_0 = "MODULATOR_CENTER.AXIS_0"
    MODULATOR_CENTER_AXIS_1 = "MODULATOR_CENTER.AXIS_1"
    COMMAND_COUNTER = "COMMAND_COUNTER"
    NAME = "NAME"


class AbstractModulatorClient(with_metaclass(abc.ABCMeta, object)):
    """Prisma-shaped client API for a PWFS modulator (not a 2-DoF DM)."""

    @abc.abstractmethod
    @returns(float)
    def getFrequencyInHz(self):
        assert False

    @abc.abstractmethod
    @returns(float)
    def getRadiusInMilliRad(self):
        assert False

    @abc.abstractmethod
    @returnsForExample(np.zeros(2))
    def getCenterInMilliRad(self):
        assert False

    @abc.abstractmethod
    @returnsNone
    def setFrequencyInHz(self, freqInHz):
        assert False

    @abc.abstractmethod
    @returnsNone
    def setRadiusInMilliRad(self, radiusInMilliRad):
        assert False

    @abc.abstractmethod
    @returnsNone
    def setCenterInMilliRad(self, centerInMilliRad):
        assert False

    @abc.abstractmethod
    @returnsNone
    def offsetCenterByMilliRad(self, offsetInMilliRad):
        assert False

    @abc.abstractmethod
    def getDiagnosticData(self):
        assert False

    @abc.abstractmethod
    @returns(ModulatorStatus)
    def getStatus(self):
        assert False

    @abc.abstractmethod
    def getSnapshot(self, prefix):
        assert False
