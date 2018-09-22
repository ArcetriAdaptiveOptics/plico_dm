#!/usr/bin/env python

from plico.client.hackerable_client import HackerableClient
from palpao.client.abstract_deformable_mirror_client import \
    AbstractDeformableMirrorClient
from plico.rpc.abstract_remote_procedure_call import \
    AbstractRemoteProcedureCall
from plico.utils.logger import Logger
from plico.utils.decorator import override, returns
from palpao.utils.timeout import Timeout
from palpao.types.deformable_mirror_status import DeformableMirrorStatus
from plico.client.serverinfo_client import ServerInfoClient


__version__= "$Id: deformable_mirror_client.py 45 2018-04-21 17:56:18Z lbusoni $"


class DeformableMirrorClient(AbstractDeformableMirrorClient,
                             HackerableClient, ServerInfoClient):

    def __init__(self,
                 rpcHandler,
                 sockets):
        assert isinstance(rpcHandler, AbstractRemoteProcedureCall)

        self._rpcHandler= rpcHandler
        self._requestSocket= sockets.serverRequest()
        self._statusSocket= sockets.serverStatus()
        self._logger= Logger.of('Camera client')

        HackerableClient.__init__(self,
                                  self._rpcHandler,
                                  self._requestSocket,
                                  self._logger)
        ServerInfoClient.__init__(self,
                                  self._rpcHandler,
                                  self._requestSocket,
                                  self._logger)


    @override
    def applyZonalCommand(self,
                          actuatorPosition,
                          timeoutInSec=Timeout.MIRROR_SET_COMMAND):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'setZonalCommand', [actuatorPosition],
            timeout=timeoutInSec)
        pass


    @override
    def getZonalCommand(self, timeoutInSec=Timeout.MIRROR_GET_ZONAL_COMMAND):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'getZonalCommand', [],
            timeout=timeoutInSec)



    @override
    @returns(DeformableMirrorStatus)
    def getStatus(self, timeoutInSec=Timeout.MIRROR_GET_STATUS):
        return self._rpcHandler.receivePickable(
            self._statusSocket,
            timeoutInSec)


    @override
    def getSnapshot(self,
                    prefix,
                    timeoutInSec=Timeout.MIRROR_GET_STATUS):
        return self._rpcHandler.sendRequest(
            self._requestSocket,
            'getSnapshot', [prefix],
            timeout=timeoutInSec)
