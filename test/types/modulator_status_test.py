#!/usr/bin/env python
import unittest
from plico_dm.types.modulator_status import ModulatorStatus
import numpy as np


class ModulatorStatusTest(unittest.TestCase):

    def testRepr(self):
        status = ModulatorStatus(20.0, 1.0, np.zeros(2), name='sim')
        text = repr(status)
        self.assertIn('sim', text)
        self.assertIn('20.0', text)


if __name__ == '__main__':
    unittest.main()
