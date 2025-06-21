# This file is a part of Tarkash
# Copyright 2015-2024 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from swayam import Driver, Template
from swayam.inject.template.builtin.internal.Cue import CueAsArg

def until(*, invoker, cue):
    cue_met = False
    counter = 0
    while not cue_met:
        if invoker.vault.has_cue_result(cue):
            cue_met = invoker.vault.get_cue_result(cue)
            if cue_met:
                break
        else:
            cue_met = False
        counter += 1
        yield Template.Counter(counter=counter)

Until = Driver.build("Until", 
                    callable=until,
                    in_template=CueAsArg, 
                    out_template=Template.Counter)

