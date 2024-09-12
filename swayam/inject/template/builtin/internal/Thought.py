# This file is a part of Swayam
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

from typing import Union, List
from pydantic import BaseModel, Field

from .Frame import FrameModel

from swayam import Template
from .Repeater import RepeaterModel

class ThoughtModel(FrameModel):
    expressions: List[Union[str, RepeaterModel]] = Field(..., description="Expression definition names that are included in this thought. Instead of a name it can be dictionary of a RepeatedDefinition.")
    purpose: Union[str,None] = Field(None, description="A statement describing the purpose of the thought.")
    directive: str = Field(None, description="Directive text for the narrative this thought builds. Extends previous directives if any.")
    actions: List[str] = Field([], title="Common Actions", description="List of actions to be used in the expressions that don't have an action list of their own.")
    
Thought = Template.build("Thought", model=ThoughtModel)