# ===============================================================================
# Copyright 2018 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
from traits.api import Enum, Float, Property, List, HasTraits, Str, Int
from pychron.hardware import get_float
from pychron.hardware.core.core_device import CoreDevice
import re
from time import sleep

IDN_RE = re.compile(r'\w{4},\w{8},\w{7}\/[\w\#]{7},\d.\d')

PRED_RE = re.compile(r'(?P<name>[A-Za-z])')


class RangeTest:
    def __init__(self, r, test):
        self._r = int(r)
        self._test = test
        self._attr = None
        match = PRED_RE.search(test)
        if match:
            self._attr = match.group('name')

    def test(self, v):
        if self._attr and eval(self._test, {self._attr: v}):
            return self._r


class LakeShoreDevice(HasTraits):
    address = Int
    setpoint = Float
    setpoint_readback = Float
    input_readback = Float
    threshold = 1

    def setpoint_achieved(self, controller, threshold=None):
        if threshold is None:
            threshold = self.threshold
        v = controller.read_input(self.address)
        return abs(v - self.setpoint) > threshold


class LakeShoreController(CoreDevice):
    devices = List(LakeShoreDevice)
    range_tests = List

    def load_additional_args(self, config):
        self.set_attribute(config, 'units', 'General', 'units', default='K')

        # [Range]
        # 1=v<10
        # 2=10<v<30
        # 3=v>30

        if config.has_section('Range'):
            items = config.items('Range')

        else:
            items = [(1, 'v<10'), (2, '10<v<30'), (3, 'v>30')]

        if items:
            self.range_tests = [RangeTest(*i) for i in items]

            # just hardcoding now. should be in config file
            dev_items = [1, 2, 3, 4]
            self._load_devices(dev_items)
        return True

    def initialize(self, *args, **kw):
        return True

    def _load_devices(self, items):
        devs = []
        for item in items:
            # instead of a factory function
            # just instantiate the object here
            dev = LakeShoreDevice(address=item)
            # dev = self._device_factory(item)
        devs.append(dev)
        self.devices = devs

    def setpoints_achieved(self, devs=None):
        if devs is None:
            devs = self.devices

        for d in devs:
            if not dev.setpoint_achieved(self):
                return False
        else:
            return True

    @get_float(default=0)
    def read_input(self, tag, mode='C', verbose=False):
        return self.ask('{}RDG? {}'.format(mode, tag), verbose=verbose)

    # def _device_factory(self, address):

        # dev = LakeShoreDevice(address=address)
        # return dev
# ============= EOF =============================================
