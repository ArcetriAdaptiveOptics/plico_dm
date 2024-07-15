'''
Mapping from DM type string to a module/class
that can act as a specialized client for that DM type
'''
from plico.client.discovery import ClientMapType


client_map = {

   'SPLATT': ClientMapType(modulename='plico_dm.client.splatt_client', classname='SPLATTClient'),
   'SimulatedDeformableMirror': ClientMapType(modulename='plico_dm.client.splatt_client', classname='SPLATTClient'),
}
