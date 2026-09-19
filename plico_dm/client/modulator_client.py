#!/usr/bin/env python
import numpy as np
from plico.client.hackerable_client import HackerableClient
from plico.client.serverinfo_client import ServerInfoClient
from plico.rpc.abstract_remote_procedure_call import \
    AbstractRemoteProcedureCall
from plico.utils.logger import Logger
from plico.utils.decorator import override, returns, returnsNone, \
    returnsForExample
from plico.utils.snapshotable import Snapshotable
from plico_dm.client.abstract_modulator_client import (
    AbstractModulatorClient, SnapshotEntry)
from plico_dm.types.modulator_status import ModulatorStatus
from plico_dm.utils.timeout import Timeout


class ModulatorClient(AbstractModulatorClient,
                      HackerableClient, ServerInfoClient):
    """ZMQ client for the plico_dm_server modulator controller."""

    def __init__(self, rpcHandler, sockets):
        assert isinstance(rpcHandler, AbstractRemoteProcedureCall)
        self._rpcHandler = rpcHandler
        self._requestSocket = sockets.serverRequest()
        self._statusSocket = sockets.serverStatus()
        self._logger = Logger.of('ModulatorClient')
        HackerableClient.__init__(self,
                                  self._rpcHandler,
                                  self._requestSocket,
                                  self._logger)
        ServerInfoClient.__init__(self,
                                  self._rpcHandler,
                                  self._requestSocket,
                                  self._logger)

    @override
    @returns(ModulatorStatus)
    def getStatus(self, timeoutInSec=Timeout.MODULATOR_GET_STATUS):
        return self._rpcHandler.receivePickable(
            self._statusSocket,
            timeoutInSec)

    @override
    @returns(float)
    def getFrequencyInHz(self):
        return float(self.getStatus().modulatorFrequencyInHz)

    @override
    @returnsNone
    def setFrequencyInHz(
            self, frequencyInHz,
            timeoutInSec=Timeout.MODULATOR_SET_FREQUENCY):
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'setModulatorFrequencyInHz',
            [float(frequencyInHz)], timeout=timeoutInSec)

    @override
    @returns(float)
    def getRadiusInMilliRad(self):
        return float(self.getStatus().modulatorRadiusInMilliRad)

    @override
    @returnsNone
    def setRadiusInMilliRad(
            self, radiusInMilliRad,
            timeoutInSec=Timeout.MODULATOR_SET_RADIUS):
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'setModulatorRadiusInMilliRad',
            [float(radiusInMilliRad)], timeout=timeoutInSec)

    @override
    @returnsForExample(np.zeros(2))
    def getCenterInMilliRad(self):
        return self.getStatus().modulatorCenterInMilliRad

    @override
    @returnsNone
    def setCenterInMilliRad(
            self, centerInMilliRad,
            timeoutInSec=Timeout.MODULATOR_SET_CENTER):
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'setModulatorCenterInMilliRad',
            [centerInMilliRad], timeout=timeoutInSec)

    @override
    @returnsNone
    def offsetCenterByMilliRad(
            self, offsetInMilliRad,
            timeoutInSec=Timeout.MODULATOR_SET_CENTER):
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'offsetModulatorCenterByMilliRad',
            [offsetInMilliRad], timeout=timeoutInSec)

    @override
    def getDiagnosticData(
            self, timeoutInSec=Timeout.MODULATOR_GET_DIAGNOSTIC_DATA):
        return self._rpcHandler.sendRequest(
            self._requestSocket, 'getModulatorDiagnosticData',
            [], timeout=timeoutInSec)

    @override
    def getSnapshot(self,
                    prefix,
                    timeoutSec=Timeout.MODULATOR_GET_STATUS):
        status = self.getStatus(timeoutInSec=timeoutSec)
        self._logger.notice("Getting snapshot for %s " % prefix)
        return self._createSnapshotFromStatus(prefix, status)

    def _createSnapshotFromStatus(self, prefix, status):
        assert isinstance(status, ModulatorStatus)
        snapshot = {}
        snapshot[SnapshotEntry.MODULATOR_CENTER_AXIS_0] = \
            status.modulatorCenterInMilliRad[0]
        snapshot[SnapshotEntry.MODULATOR_CENTER_AXIS_1] = \
            status.modulatorCenterInMilliRad[1]
        snapshot[SnapshotEntry.MODULATOR_AMPLITUDE] = \
            status.modulatorRadiusInMilliRad
        snapshot[SnapshotEntry.MODULATOR_FREQUENCY] = \
            status.modulatorFrequencyInHz
        snapshot[SnapshotEntry.COMMAND_COUNTER] = status.command_counter
        snapshot[SnapshotEntry.NAME] = status.name
        return Snapshotable.prepend(prefix, snapshot)
