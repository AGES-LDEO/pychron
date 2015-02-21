# ===============================================================================
# Copyright 2014 Jake Ross
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

# ============= enthought library imports =======================
from pyface.tasks.traits_editor import TraitsEditor
from traits.api import HasTraits, Button
from traitsui.api import View, Item, UItem, InstanceEditor
# ============= standard library imports ========================
# ============= local library imports  ==========================


class ScanEditor(TraitsEditor):
    id = 'pychron.scan'

    def traits_view(self):
        v = View(UItem('graph', style='custom', editor=InstanceEditor()))
        return v


class PeakCenterEditor(ScanEditor):
    pass


class CoincidenceEditor(ScanEditor):
    pass



# ============= EOF =============================================


