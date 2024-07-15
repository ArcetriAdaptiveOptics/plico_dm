#!/usr/bin/env python

from plico_dm.client.deformable_mirror_client import DeformableMirrorClient
from plico_dm.utils.timeout import Timeout


class SPLATTClient(DeformableMirrorClient):

    def __init__(self, rpcHandler, sockets):
        super().__init__(rpcHandler, sockets)

    def get_capsens(self, timeoutInSec=Timeout.GENERIC_COMMAND):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'get_capsens', [],
            timeout=timeoutInSec)

