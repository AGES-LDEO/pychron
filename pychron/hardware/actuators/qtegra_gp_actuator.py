# ===============================================================================
# Copyright 2011 Jake Ross
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

#========== standard library imports ==========

#========== local library imports =============
from __future__ import absolute_import

from pychron.hardware.actuators import get_valve_address
from .gp_actuator import GPActuator
from pychron.globals import globalv
# ========== local library imports =============
from __future__ import absolute_import

from pychron.globals import globalv
from pychron.hardware.actuators import get_valve_address
from .gp_actuator import GPActuator


class QtegraGPActuator(GPActuator):
    """

    """

    def get_state_checksum(self, keys):
        return 0

    def get_channel_state(self, obj, verbose=False, **kw):
        """
        """

        cmd = 'GetValveState {}'.format(get_valve_address(obj))

        s = self.ask(cmd, verbose=verbose)

        if s is not None:
            return s.strip() == 'True'

    def close_channel(self, obj):
        """
        """

        cmd = 'Close {}'.format(get_valve_address(obj))

        r = self.ask(cmd)
        if r is None and globalv.communication_simulation:
            return True

        if r is not None and r.strip() == 'OK':
            return self.get_channel_state(obj) is False

    def open_channel(self, obj):
        """
        """
        cmd = 'Open {}'.format(get_valve_address(obj))

        r = self.ask(cmd)
        if r is None and globalv.communication_simulation:
            return True

        if r is not None and r.strip() == 'OK':
            return self.get_channel_state(obj) is True

# ============= EOF =====================================
