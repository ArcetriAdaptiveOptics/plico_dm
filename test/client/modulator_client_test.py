#!/usr/bin/env python
import unittest
import numpy as np
from plico.utils.decorator import override
from plico.rpc.dummy_remote_procedure_call import DummyRpcHandler
from plico.rpc.dummy_sockets import DummySockets
from plico_dm.client.modulator_client import ModulatorClient
from plico_dm.client.abstract_modulator_client import SnapshotEntry
from plico_dm.client.simulated_modulator_client import SimulatedModulatorClient
from plico_dm.types.modulator_status import ModulatorStatus
from plico_dm.utils.timeout import Timeout


class TesterRpcHandler(DummyRpcHandler):

    def __init__(self):
        self._sendRequestHistory = []
        self._receivePickableHistory = []
        self._objToReturnWithReceivePickable = None

    @override
    def sendRequest(self, socket, command, args, timeout=1):
        self._sendRequestHistory.append(
            (socket, command, args, timeout))

    @override
    def receivePickable(self, socket, timeout=1):
        self._receivePickableHistory.append((socket, timeout))
        return self._objToReturnWithReceivePickable

    def getLastSendRequestArguments(self):
        return self._sendRequestHistory[-1]

    def wantsPickable(self, obj):
        self._objToReturnWithReceivePickable = obj


class ModulatorClientTest(unittest.TestCase):

    def setUp(self):
        self._rpc = TesterRpcHandler()
        self._sockets = DummySockets()
        self._client = ModulatorClient(self._rpc, self._sockets)

    def testSetRadius(self):
        self._client.setRadiusInMilliRad(1.5)
        self.assertEqual(
            self._rpc.getLastSendRequestArguments(),
            (self._sockets.serverRequest(),
             'setModulatorRadiusInMilliRad',
             [1.5],
             Timeout.MODULATOR_SET_RADIUS))

    def testSetFrequency(self):
        self._client.setFrequencyInHz(42.0)
        self.assertEqual(
            self._rpc.getLastSendRequestArguments(),
            (self._sockets.serverRequest(),
             'setModulatorFrequencyInHz',
             [42.0],
             Timeout.MODULATOR_SET_FREQUENCY))

    def testSetCenter(self):
        center = np.array([0.1, -0.2])
        self._client.setCenterInMilliRad(center)
        sock, cmd, args, timeout = self._rpc.getLastSendRequestArguments()
        self.assertEqual(sock, self._sockets.serverRequest())
        self.assertEqual(cmd, 'setModulatorCenterInMilliRad')
        np.testing.assert_array_equal(args[0], center)
        self.assertEqual(timeout, Timeout.MODULATOR_SET_CENTER)

    def testGetStatusFields(self):
        status = ModulatorStatus(20.0, 1.25, np.array([0.0, 0.5]),
                                 command_counter=3, name='sim')
        self._rpc.wantsPickable(status)
        self.assertEqual(20.0, self._client.getFrequencyInHz())
        self.assertEqual(1.25, self._client.getRadiusInMilliRad())
        np.testing.assert_array_equal(
            np.array([0.0, 0.5]), self._client.getCenterInMilliRad())

    def testGetSnapshot(self):
        status = ModulatorStatus(1975.0, 2.0, np.array([-1.0, 3.0]),
                                 command_counter=1, name='lab')
        self._rpc.wantsPickable(status)
        snapshot = self._client.getSnapshot('baar')
        self.assertEqual(
            1975.0,
            snapshot['baar.%s' % SnapshotEntry.MODULATOR_FREQUENCY])
        self.assertEqual(
            2.0,
            snapshot['baar.%s' % SnapshotEntry.MODULATOR_AMPLITUDE])


class SimulatedModulatorClientTest(unittest.TestCase):

    def testSetGetRoundTrip(self):
        client = SimulatedModulatorClient('unit')
        client.setRadiusInMilliRad(2.5)
        client.setFrequencyInHz(55.0)
        client.setCenterInMilliRad(np.array([0.1, -0.2]))
        self.assertEqual(2.5, client.getRadiusInMilliRad())
        self.assertEqual(55.0, client.getFrequencyInHz())
        np.testing.assert_array_almost_equal(
            np.array([0.1, -0.2]), client.getCenterInMilliRad())
        client.offsetCenterByMilliRad(np.array([0.05, 0.05]))
        np.testing.assert_array_almost_equal(
            np.array([0.15, -0.15]), client.getCenterInMilliRad())
        diagn = client.getDiagnosticData()
        self.assertEqual((9, 4000), diagn.shape)


if __name__ == '__main__':
    unittest.main()
