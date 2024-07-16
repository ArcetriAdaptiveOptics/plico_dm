#!/usr/bin/env python

from plico_dm.client.deformable_mirror_client import DeformableMirrorClient
from plico_dm.utils.timeout import Timeout


class SPLATTClient(DeformableMirrorClient):

    def __init__(self, rpcHandler, sockets):
        super().__init__(rpcHandler, sockets)

    def get_capsens(self, timeoutInSec=Timeout.SPLATT_COMMAND):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'get_capsens', [],
            timeout=timeoutInSec)

    def set_shell(self, timeoutInSec=Timeout.SPLATT_SET):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'set_shell', [],
            timeout=timeoutInSec)

    def send_command(self, cmd, timeoutInSec=Timeout.SPLATT_COMMAND):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'send_matlab_command', [cmd],
            timeout=timeoutInSec)

    def get_data(self, cmd, timeoutInSec=Timeout.SPLATT_COMMAND):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'get_matlab_data', [cmd],
            timeout=timeoutInSec)

