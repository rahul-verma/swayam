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

from swayam.inject.driver import Driver
from swayam import Action

import os
from swayam import Driver, Template
from swayam.inject.template.builtin.internal.DraftDependency import DraftDependency
from swayam.inject.template.builtin.internal.Injectable import Injectable

def draft_loop(*, invoker, name, args=None):
    from swayam import Action
    from swayam import Draft
    from swayam.llm.phase.expression.drafter import Drafter as DraftWriter
    draft = getattr(Draft, name)
    drafter = DraftWriter(draft_info=draft)
    invoker.phase.drafter = drafter

    if draft.dependencies:
        for dependency in draft.dependencies:
            contents = dependency.load()
            yield DraftDependency(
                dependency_description=dependency.description,
                dependency_template=dependency.template.definition,
                dependency_content=contents
            )
    else:
        yield DraftDependency(
                dependency_description="",
                dependency_template="",
                dependency_content=""
            )

Drafter = Driver.build("Drafter", 
                        callable=draft_loop,
                        in_template=Injectable, 
                        out_template=DraftDependency)

