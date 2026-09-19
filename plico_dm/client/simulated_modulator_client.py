#!/usr/bin/env python
"""In-process simulated modulator client (no ZMQ / no hardware).

Useful for laptop unit tests and REPL smoke without starting plico_dm_server.
"""
import numpy as np
from plico.utils.decorator import override, returns, returnsNone, \
    returnsForExample
from plico.utils.snapshotable import Snapshotable
from plico_dm.client.abstract_modulator_client import (
    AbstractModulatorClient, SnapshotEntry)
from plico_dm.types.modulator_status import ModulatorStatus


class SimulatedModulatorClient(AbstractModulatorClient):

    def __init__(self, name='SimulatedModulator'):
        self._name = name
        self._radiusInMilliRad = 10.
        self._frequencyInHz = 100.
        self._centerInMilliRad = np.zeros(2)
        self._command_counter = 0

    def _bump(self):
        self._command_counter += 1

    @override
    def getFrequencyInHz(self):
        return float(self._frequencyInHz)

    @override
    def getRadiusInMilliRad(self):
        return float(self._radiusInMilliRad)

    @override
    @returnsForExample(np.zeros(2))
    def getCenterInMilliRad(self):
        return self._centerInMilliRad.copy()

    @override
    @returnsNone
    def setFrequencyInHz(self, freqInHz):
        self._frequencyInHz = float(freqInHz)
        self._bump()

    @override
    @returnsNone
    def setRadiusInMilliRad(self, radiusInMilliRad):
        self._radiusInMilliRad = float(radiusInMilliRad)
        self._bump()

    @override
    @returnsNone
    def setCenterInMilliRad(self, centerInMilliRad):
        self._centerInMilliRad = np.asarray(centerInMilliRad, dtype=float)
        self._bump()

    @override
    @returnsNone
    def offsetCenterByMilliRad(self, offsetInMilliRad):
        self.setCenterInMilliRad(
            self.getCenterInMilliRad() + np.asarray(offsetInMilliRad,
                                                    dtype=float))

    @override
    def getDiagnosticData(self):
        nPoints = 4000
        dt = 40e-6
        t = np.linspace(0, dt * nPoints, nPoints, endpoint=False)
        x = (self._radiusInMilliRad *
             np.sin(t * self._frequencyInHz * 2 * np.pi) +
             self._centerInMilliRad[0])
        y = (self._radiusInMilliRad *
             np.cos(t * self._frequencyInHz * 2 * np.pi) +
             self._centerInMilliRad[1])
        diagnArray = np.zeros((9, nPoints))
        diagnArray[0] = t
        diagnArray[1] = x
        diagnArray[2] = y
        diagnArray[5] = x
        diagnArray[6] = y
        return diagnArray

    @override
    @returns(ModulatorStatus)
    def getStatus(self):
        return ModulatorStatus(
            self._frequencyInHz,
            self._radiusInMilliRad,
            self._centerInMilliRad.copy(),
            command_counter=self._command_counter,
            name=self._name)

    @override
    def getSnapshot(self, prefix):
        status = self.getStatus()
        snapshot = {
            SnapshotEntry.MODULATOR_CENTER_AXIS_0:
                status.modulatorCenterInMilliRad[0],
            SnapshotEntry.MODULATOR_CENTER_AXIS_1:
                status.modulatorCenterInMilliRad[1],
            SnapshotEntry.MODULATOR_AMPLITUDE:
                status.modulatorRadiusInMilliRad,
            SnapshotEntry.MODULATOR_FREQUENCY:
                status.modulatorFrequencyInHz,
            SnapshotEntry.COMMAND_COUNTER: status.command_counter,
            SnapshotEntry.NAME: status.name,
        }
        return Snapshotable.prepend(prefix, snapshot)
