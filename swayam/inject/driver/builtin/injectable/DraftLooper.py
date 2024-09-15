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
from swayam import Driver, Template, Reference
from swayam.inject.template.builtin.internal.Reference import Reference as ReferenceTemplate
from swayam.inject.template.builtin.internal.Injectable import InjectableModel

def draft_loop(*, invoker, entity_name):
    from swayam import Action
    from swayam import Artifact
    from swayam.llm.phase.expression.drafter import Drafter
    draft = getattr(Artifact, entity_name)
    drafter = Drafter(artifact=draft, thought=invoker.thought_name)
    invoker.phase.drafter = drafter
    if not draft.has_dependencies:
        yield ReferenceTemplate(
                            reference_description="",
                            reference_template="",
                            reference_content=""
                        )
    else:
        
        # Handle references
        for reference in draft.references:
            if isinstance(reference, str):
                reference = getattr(Reference, reference)(thought=invoker.thought_name)
                contents = reference.load()
                yield ReferenceTemplate(
                    reference_description=reference.description,
                    reference_template=json.dumps(reference.template.definition),
                    reference_content=json.dumps(contents),
                    reference_writeup=reference.plural_writeup(contents)
                )   
            else:
                reference = getattr(Reference, reference.name)
                contents = reference.load()
                if reference.iter_content:
                    for content in contents:
                        yield ReferenceTemplate(
                            reference_description=reference.description,
                            reference_template=json.dumps(reference.template.definition),
                            reference_content=json.dumps(content),
                            reference_writeup=reference.singular_writeup(content)
                        ) 
                else:
                    for content in contents:
                        yield ReferenceTemplate(
                            reference_description=reference.description,
                            reference_template=json.dumps(reference.template.definition),
                            reference_content=json.dumps(content),
                            reference_writeup=reference.singular_writeup(content)
                        )

DraftLooper = Driver.build("DraftLooper", 
                        callable=draft_loop,
                        in_template=Template.EntityName, 
                        out_template=ReferenceTemplate)

