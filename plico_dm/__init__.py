
from plico.client.discovery import plico_list, plico_get, plico_client
from plico_dm.client.client_map import client_map
from plico_dm.client.deformable_mirror_client import DeformableMirrorClient
from plico_dm.client.modulator_client import ModulatorClient
from plico_dm.client.simulated_modulator_client import SimulatedModulatorClient
from plico_dm.utils.constants import Constants


def _getDefaultConfigFilePath():
    from plico.utils.config_file_manager import ConfigFileManager
    cfgFileMgr= ConfigFileManager(Constants.APP_NAME,
                                  Constants.APP_AUTHOR,
                                  Constants.THIS_PACKAGE)
    return cfgFileMgr.getConfigFilePath()


defaultConfigFilePath= _getDefaultConfigFilePath()


def deformableMirror(hostname, port):
    '''Generic DeformableMirrorClient, kept for backward compatibility'''
    return plico_client(DeformableMirrorClient, hostname, port)


def modulator(hostname, port):
    '''Prisma-shaped ModulatorClient for a PWFS modulator server.'''
    return plico_client(ModulatorClient, hostname, port)


def simulated_modulator(name='SimulatedModulator'):
    '''In-process simulated modulator (no server / no hardware).'''
    return SimulatedModulatorClient(name=name)


def list_dms(timeout_in_seconds=2):
    '''List all available plico DM servers'''
    return plico_list(server_type='plico_dm', timeout_in_seconds=timeout_in_seconds)


def get(dm_name, timeout_in_seconds=2):
    '''Get a client for a specific DM server'''
    return plico_get(server_type='plico_dm', name=dm_name, default_class=DeformableMirrorClient,
               timeout_in_seconds=timeout_in_seconds, client_map=client_map)

