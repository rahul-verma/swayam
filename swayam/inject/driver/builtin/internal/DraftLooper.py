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
from swayam.inject.template.builtin.injectable.Reference import Reference as ReferenceTemplate
from swayam.inject.template.builtin.injectable.Reference import ReferenceContent
from swayam.inject.template.builtin.internal.Injectable import InjectableModel
from swayam.inject.template.template import Data



from swayam import Action, Template
from swayam.inject.template.builtin import *

import os
import re

def call_drafter(*, invoker, **kwargs):
    invoker.phase.drafter.draft(kwargs)
    return Template.Success()

def draft_loop(*, invoker, definitions, artifact, reset_conversation=True, mode="overwrite", draft_name=None):
    from swayam import Action
    from swayam import Artifact
    from swayam.llm.phase.expression.drafter import Drafter
    artifact = getattr(Artifact, artifact)
    drafter = Drafter(artifact=artifact, thought=invoker.thought_name, mode=mode, draft_name=draft_name)
    invoker.phase.drafter = drafter
    
    Draft = Action.build("Draft", 
                         callable=call_drafter, 
                         description=f"Writes the {artifact.singular_name} to disk.",
                         in_template=artifact.template,
                         out_template=Template.Result
    )
    
    invoker.phase.mandatory_action = Draft
    
    if not artifact.has_dependencies:
        yield ReferenceTemplate(
                            reference_description="",
                            reference_template="",
                            reference_content=""
                        )
    else:
        for feeder in artifact.feeders:
            feed_driver = None
            feed_template = None
            if isinstance(feeder, str):
                feed_driver = getattr(Driver, feeder)
                feed_template = feed_driver.out_template
                feed_driver = feed_driver()
            else:
                feeder_name = feeder["name"]
                feed_driver = getattr(Driver, feeder_name)
                feed_template = feed_driver.out_template
                feed_driver = feed_driver(**feeder["args"])

            for content in feed_driver:
                yield feed_template(**content)
            
        def get_reference(name):
            from swayam.inject.reference.error import ReferenceContentNotFoundError
            try:
                return getattr(Reference, name)
            except ReferenceContentNotFoundError:
                # Look in Thought's Drafts
                from tarkash import Tarkash
                from swayam.core.constant import SwayamOption
                folio_draft_dir = Tarkash.get_option_value(SwayamOption.FOLIO_DRAFT_DIR)
                reference_file_path = os.path.join(folio_draft_dir, invoker.phase.thought_name, name + ".json")
                if os.path.exists(reference_file_path): 
                    from swayam.inject.reference.reference import Reference as ReferenceObject
                    return ReferenceObject(name, file_path=reference_file_path)
                else:
                    raise ReferenceContentNotFoundError(name=name)
                
        def create_prompt_formatter(ref, content, whole_reference=True):
            if whole_reference:
                writeup = reference.plural_writeup()
                reference_data = dict()
            else:
                writeup = reference.singular_writeup(content)
                reference_data = content
            return ReferenceTemplate(
                    reference_description=ref.description,
                    reference_template=json.dumps(ref.template.definition),
                    reference_content=json.dumps(content),
                    reference_writeup=writeup,
                    reference_data=reference_data
                ) 
                           

        # Handle references
        for reference_data in artifact.references:
            from swayam import Reference
            if isinstance(reference_data, str):
                ref_name = reference_data
                reference = get_reference(ref_name)
                yield create_prompt_formatter(reference, reference.contents, whole_reference=True)
            else:
                ref_name = reference_data["name"]
                iter_content = reference_data.get("iter_content", False)
                reference = get_reference(ref_name)
                if iter_content:
                    for content in reference.contents:
                        yield create_prompt_formatter(reference, content, whole_reference=False) 
                else:
                    yield create_prompt_formatter(reference, reference.contents, whole_reference=True)

from swayam.inject.template.builtin.internal import DrafterTemplate

DraftLooper = Driver.build("DraftLooper", 
                        callable=draft_loop,
                        in_template=DrafterTemplate, 
                        out_template=ReferenceContent)

