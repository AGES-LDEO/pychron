# ===============================================================================
# Copyright 2019 ross
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
from pychron.options.options_manager import OptionsController, ArArCalculationsOptionsManager
from pychron.options.views.views import view
from pychron.pipeline.nodes.base import BaseNode


class ArArCalculationsNode(BaseNode):
    name = 'ArArCalculations'

    def run(self, state):
        state.arar_calculation_options = self.options

    def configure(self, pre_run=False, **kw):
        model = ArArCalculationsOptionsManager()
        info = OptionsController(model=model).edit_traits(view=view('{} Options'.format(self.name)),
                                                          kind='livemodal')
        if info.result:
            self.options = model.selected_options
            return True

# ============= EOF =============================================
