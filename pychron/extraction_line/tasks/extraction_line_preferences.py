# ===============================================================================
# Copyright 2013 Jake Ross
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
import os

from traits.api import Str, Bool, Int
from traitsui.api import View, Item, VGroup, HGroup, spring
from envisage.ui.tasks.preferences_pane import PreferencesPane
from traitsui.editors import FileEditor
from traitsui.group import Tabbed
from traitsui.item import UItem


# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.core.ui.custom_label_editor import CustomLabel
from pychron.envisage.tasks.base_preferences_helper import BasePreferencesHelper, BaseConsolePreferences, \
    BaseConsolePreferencesPane
from pychron.paths import paths


class ConsolePreferences(BaseConsolePreferences):
    preferences_path = 'pychron.extraction_line.console'


class ConsolePreferencesPane(BaseConsolePreferencesPane):
    model_factory = ConsolePreferences
    label = 'Extraction Line'

    def traits_view(self):
        preview = CustomLabel('preview',
                              size_name='fontsize',
                              color_name='textcolor',
                              bgcolor_name='bgcolor')

        v = View(VGroup(HGroup(UItem('fontsize'),
                               UItem('textcolor'),
                               UItem('bgcolor')),
                        preview,
                        show_border=True,
                        label=self.label))
        return v


class ExtractionLinePreferences(BasePreferencesHelper):
    name = 'ExtractionLine'
    preferences_path = 'pychron.extraction_line'
    id = 'pychron.extraction_line.preferences_page'
    check_master_owner = Bool
    use_network = Bool
    inherit_state = Bool
    display_volume = Bool
    volume_key = Str

    use_status_monitor = Bool
    valve_state_frequency = Int
    valve_lock_frequency = Int
    valve_owner_frequency = Int
    update_period = Int
    gauge_update_period = Int
    use_gauge_update = Bool

    canvas_path = Str
    canvas_config_path = Str
    valves_path = Str
    checksum_frequency = Int


class ExtractionLinePreferencesPane(PreferencesPane):
    model_factory = ExtractionLinePreferences
    category = 'ExtractionLine'

    def traits_view(self):
        n_grp = VGroup(
            Item('use_network',
                 tooltip='Flood the extraction line with the maximum state color'),
            VGroup(
                Item('inherit_state',
                     tooltip='Should the valves inherit the maximum state color'),
                enabled_when='use_network'),
            VGroup(
                HGroup(
                    Item('display_volume',
                         tooltip='Display the volume for selected section. \
Hover over section and hit the defined volume key (default="v")'),
                    Item('volume_key',
                         tooltip='Hit this key to display volume',
                         label='Key',
                         width=50,
                         enabled_when='display_volume'),
                    spring, ),
                label='volume',
                enabled_when='use_network'),
            label='Network')

        s_grp = VGroup(Item('use_status_monitor'),
                       VGroup(Item('update_period', tooltip='Delay between iterations in seconds'),
                              VGroup(
                                  Item('valve_state_frequency', label='State',
                                       tooltip='Check Valve State, i.e Open or Closed every N iterations'),
                                  Item('checksum_frequency', label='Checksum',
                                       tooltip='Check the entire extraction line state every N iterations'),
                                  Item('valve_lock_frequency', label='Lock',
                                       tooltip='Check Valve Software Lock. i.e Locked or unlocked every N iterations'),
                                  Item('valve_owner_frequency', label='Owner',
                                       tooltip='Check Valve Owner every N iterations'),
                                  label='Frequencies'),
                              enabled_when='use_status_monitor'),
                       label='Status Monitor')

        v_grp = VGroup(
            Item('check_master_owner',
                 label='Check Master Ownership',
                 tooltip='Check valve ownership even if this is the master computer'),
            n_grp,
            s_grp,
            show_border=True,
            label='Valves')
        g_grp = VGroup(Item('use_gauge_update',
                            label='Use Gauge Update',
                            tooltip='Start a timer to periodically update the gauge pressures'),
                       Item('gauge_update_period',
                            label='Period',
                            tooltip='Delay between updates in seconds. '
                                    'Set to 0 to use the gauge controllers configured value.',
                            enabled_when='use_gauge_update'),
                       label='Gauges')

        p_grp = VGroup(Item('canvas_path', editor=FileEditor(root_path=os.path.join(paths.canvas2D_dir, 'canvas.xml'))),
                       Item('canvas_config_path', editor=FileEditor()),
                       Item('valves_path', editor=FileEditor(root_path=os.path.join(paths.extraction_line_dir,
                                                                                    'valves.xml'))),
                       label='Paths')

        return View(Tabbed(p_grp, v_grp, g_grp))


# ============= EOF =============================================
