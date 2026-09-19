class ModulatorStatus(object):
    """Published status snapshot for a PWFS modulator controller."""

    def __init__(self,
                 modulatorFrequencyInHz,
                 modulatorRadiusInMilliRad,
                 modulatorCenterInMilliRad,
                 command_counter=0,
                 name=''):
        self.modulatorFrequencyInHz = modulatorFrequencyInHz
        self.modulatorRadiusInMilliRad = modulatorRadiusInMilliRad
        self.modulatorCenterInMilliRad = modulatorCenterInMilliRad
        self.command_counter = command_counter
        self.name = name

    def __repr__(self):
        return (
            "ModulatorStatus(name=%r, freq=%s Hz, radius=%s mrad, "
            "center=%s, command_counter=%s)" % (
                self.name,
                self.modulatorFrequencyInHz,
                self.modulatorRadiusInMilliRad,
                self.modulatorCenterInMilliRad,
                self.command_counter))
