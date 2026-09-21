
import os
import astropy.io.fits as pyfits
from plico_dm.calibration.abstract_calibration_manager import \
    AbstractCalibrationManager
from plico.utils.decorator import override, returnsNone, returns, cacheResult
from plico_dm.types.modal_basis import ModalBasis
import numpy
from plico.utils.fits_file_based_calibration_manager \
    import FitsFileBasedCalibrationManager


class CalibrationManagerException(Exception):
    pass


class CalibrationManager(AbstractCalibrationManager,
                         FitsFileBasedCalibrationManager):

    def __init__(self, calibrationRootDir):
        self._calibRootDir = calibrationRootDir

    def _checkTag(self, tag):
        if tag is None:
            raise CalibrationManagerException(
                "A tag must be given but is None")
        if len(tag) == 0:
            raise CalibrationManagerException(
                "A tag name must be valid but it is '%s'" % (tag))

    def getModalBasisFileName(self, tag):
        return os.path.join(self._calibRootDir,
                            "modal_basis",
                            "%s.fits" % tag)

    @override
    @returnsNone
    def saveModalBasis(self, tag, modalBasis):
        self._checkTag(tag)
        fileName = self.getModalBasisFileName(tag)
        self._createFoldersIfMissing(fileName)
        pyfits.writeto(fileName,
                       modalBasis.modalToZonalMatrix,
                       overwrite=False)

    @override
    @returns(ModalBasis)
    @cacheResult
    def loadModalBasis(self, tag):
        self._checkTag(tag)
        fileName = self.getModalBasisFileName(tag)
        m2z = pyfits.getdata(fileName)
        return ModalBasis(m2z)

    def getPiTipTiltCalibrationFileName(self):
        return os.path.join(self._calibRootDir,
                            "modulator/pi_calibration.py")

    def _loadPiTipTiltCalibrationModule(self):
        # Python 3.12+ removed the imp module; load calib .py via importlib.
        import importlib.util
        path = self.getPiTipTiltCalibrationFileName()
        spec = importlib.util.spec_from_file_location('pi_calibration', path)
        if spec is None or spec.loader is None:
            raise CalibrationManagerException(
                "Cannot load PI tip-tilt calibration from %s" % path)
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)
        return mm.PhysikInstrumenteCalibration()

    @override
    @cacheResult
    def loadPiTipTiltCalibration(self, serialNumber):
        pic = self._loadPiTipTiltCalibrationModule()
        return pic.getCalibrationFor(serialNumber)

    def getZonalCommandFileName(self, tag):
        return os.path.join(self._calibRootDir,
                            "zonal_command",
                            "%s.fits" % tag)

    @override
    @returnsNone
    def saveZonalCommand(self, tag, zonalCommand):
        self._checkTag(tag)
        fileName = self.getZonalCommandFileName(tag)
        self._createFoldersIfMissing(fileName)
        pyfits.writeto(fileName,
                       zonalCommand,
                       overwrite=False)

    @override
    @returns(numpy.ndarray)
    def loadZonalCommand(self, tag):
        self._checkTag(tag)
        fileName = self.getZonalCommandFileName(tag)
        return pyfits.getdata(fileName)
