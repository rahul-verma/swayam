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
from swayam import Generator, Structure
from swayam.inject.structure.builtin.internal.Condition import ConditionAsArg

def until(*, invoker, condition):
    condition_met = False
    counter = 0
    while not condition_met:
        if invoker.store.has_condition_result(condition):
            condition_met = invoker.store.get_condition_result(condition)
            if condition_met:
                break
        else:
            condition_met = False
        counter += 1
        yield Structure.Counter(counter=counter)

Until = Generator.build("Until", 
                                 callable=until,
                                 input_structure=ConditionAsArg, 
                                 output_structure=Structure.Counter)

