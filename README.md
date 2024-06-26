# plico_dm: deformable mirror controller 


 ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ArcetriAdaptiveOptics/plico_dm/python-package.yml)
 [![codecov](https://codecov.io/gh/ArcetriAdaptiveOptics/plico_dm/branch/main/graph/badge.svg?token=ApWOrs49uw)](https://codecov.io/gh/ArcetriAdaptiveOptics/plico_dm)
 [![Documentation Status](https://readthedocs.org/projects/plico_dm/badge/?version=latest)](https://plico_dm.readthedocs.io/en/latest/?badge=latest)
 [![PyPI version](https://badge.fury.io/py/plico-dm.svg)](https://badge.fury.io/py/plico-dm)


This is part a component of the [plico][plico] framework to control DMs (Alpao, MEMS)


[plico]: https://github.com/ArcetriAdaptiveOptics/plico

## Drivers
The drivers for the mirrors whose control software was developed in plico_dm can be found [here].

[here]: https://drive.google.com/drive/folders/1wjaBlFTa_893L_LjJgfgYH6o3rhrh1VR 

## Installation

### Installing


```
pip install plico_dm
```

In plico_dm source dir

```
pip install .
```

During development you want to update use

```
pip install -e .
```
that install a python egg with symlinks to the source directory in such 
a way that changes in the python code are immediately available without 
the need for re-installing (beware of conf/calib files!)

### Uninstall

```
pip uninstall plico_dm
```

### Config files

The application uses `appdirs` to locate configurations, calibrations 
and log folders: the path varies as it is OS specific. 
The configuration files are copied when the application is first used
from their original location in the python package to the final
destination, where they are supposed to be modified by the user.
The application never touches an installed file (no delete, no overwriting)

To query the system for config file location, in a python shell:

```
import plico_dm
plico_dm.defaultConfigFilePath
```


The user can specify customized conf/calib/log file path for both
servers and client (how? ask!)

## How to use it

Open a terminal and execute the following commands
```
import plico_dm
dm =  plico_dm.deformableMirror(hostServer, portServer)
```

These are the basic commands available:
- dm.get_shape(): return the actuator positions
- dm.set_shape(): set the absolute actuator positions
- dm.get_number_of_actuators(): return the DM numbers of actuators

