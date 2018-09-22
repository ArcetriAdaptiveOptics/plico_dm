import abc
from plico.utils.decorator import returnsNone, returns, returnsForExample
from palpao.types.deformable_mirror_status import DeformableMirrorStatus
from six import with_metaclass




class SnapshotEntry(object):
    COMMAND_COUNTER= "COMMAND_COUNTER"
    SERIAL_NUMBER= "SERIAL_NUMBER"
    STEP_COUNTER= "STEP_COUNTER"



class AbstractDeformableMirrorClient(with_metaclass(abc.ABCMeta, object)):
    """
    Interface to control a deformable mirror


    Assume a modal control of the DM.
    TBC: Assume the DM can apply an pure optical tip and tilt
    """

    @abc.abstractmethod
    def numberOfModes(self):
        """ Number of modes of the deformable mirror

        Return the number of modes of the deformable mirror.
        This is the number of degrees of freedom. 

        Return:
            numberOfModes (int): the number of modes of the deformable mirror.
        """
        assert False

    @abc.abstractmethod
    @returnsNone
    def setShape(self, command):
        """ Set Deformable Mirror Shape

        Send to the controller the request to set the DM shape

        Parameters:
            command (:obj:ndarray): an array containing the required value for the actuators/modes
                The size of the array must be equal to the number of modes of the DM


        """
        assert False


    @abc.abstractmethod
    def loadShapeSequence(self, shapeSequence):
        """ Load a shape sequence to be periodically applied to the mirror

        The shape sequence is added to the current shape

        Parameters:
            shapeSequence (:obj:ndarray): an array containing the shape sequence value for the actuators/modes
                The array size is (nModes, nTimeSteps)

        """
        assert False
    



    @abc.abstractmethod
    @returnsNone
    def applyZonalCommand(self, actuatorPosition):
        assert False


    @abc.abstractmethod
    def getZonalCommand(self):
        assert False


    @abc.abstractmethod
    def offsetZonalCommand(self, actuatorOffset):
        assert False


    @abc.abstractmethod
    @returnsNone
    def applyModalCommand(self, actuatorPosition):
        assert False


    @abc.abstractmethod
    def getModalCommand(self):
        assert False


    @abc.abstractmethod
    def offsetModalCommand(self, actuatorOffset):
        assert False



    @abc.abstractmethod
    @returnsForExample({'WFS_CAMERA.EXPOSURE_TIME_MS': 10})
    def getSnapshot(self, prefix):
        assert False


    @abc.abstractmethod
    @returns(DeformableMirrorStatus)
    def getStatus(self):
        assert False
