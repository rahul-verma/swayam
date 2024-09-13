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

import json
from swayam.inject.driver import Driver
from swayam import Action
from pydantic import Field, BaseModel

import os
from swayam import Driver, Template
from swayam.inject.template.builtin.internal.DraftDependency import DraftDependency
from swayam.inject.template.builtin.internal.Injectable import InjectableModel

def draft_loop(*, invoker, name, iter_content=False):
    from swayam import Action
    from swayam import Draft
    from swayam.llm.phase.expression.drafter import Drafter as DraftWriter
    draft = getattr(Draft, name)
    drafter = DraftWriter(draft_info=draft)
    invoker.phase.drafter = drafter
    if not draft.dependencies:
        yield DraftDependency(
                            draft_dependency_description="",
                            draft_dependency_template="",
                            draft_dependency_content=""
                        )
    else:
        for dependency in draft.dependencies:
            contents = dependency.load()
            if not iter_content:
                yield DraftDependency(
                    draft_dependency_description=dependency.description,
                    draft_dependency_template=json.dumps(dependency.template.definition),
                    draft_dependency_content=json.dumps(contents),
                    draft_dependency_writeup=dependency.plural_writeup(contents)
                )    
            else:
                for content in contents:
                    yield DraftDependency(
                        draft_dependency_description=dependency.description,
                        draft_dependency_template=json.dumps(dependency.template.definition),
                        draft_dependency_content=json.dumps(content),
                        draft_dependency_writeup=dependency.singular_writeup(content)
                    )    

class DraftLoopInjectable(BaseModel):
    iter_content: bool  = Field(False)
    name: str
    
DraftLoop = Template.build("DraftLoop", model = DraftLoopInjectable)

Drafter = Driver.build("Drafter", 
                        callable=draft_loop,
                        in_template=DraftLoop, 
                        out_template=DraftDependency)

