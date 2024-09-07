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

from typing import List, Union

from pydantic import BaseModel, Field
from swayam import Structure

from .Condition import ConditionModel
from .Parser import ParserModel
from .Tool import ToolModel
from .Resource import ResourceModel

class StagedResourcesModel(BaseModel):
    before_node: List[Union[str, ResourceModel, ConditionModel, ParserModel, ToolModel]]  = Field(list(), title="List of Injectable names or injectable dicts called before this phase object is communicated.", description="List of names of Resources, Conditions, Parsers or Tools to run before the target narration object in this phase.", examples=["Condition.C1", "Parser.P1", "Tool.t1"])
    after_node: List[Union[str, ResourceModel, ConditionModel, ParserModel, ToolModel]]  = Field(list(), title="List of Injectable names or injectable dicts called after this phase object is communicated.",  description="List of names of Resources, Conditions, Parsers or Tools to run after the target narration object in this phase.", examples=["Resource.R1", "Condition.C1", "Parser.P1", "Tool.t1"])
    
class FixtureModel(BaseModel):
    before: List[Union[str, ResourceModel, ConditionModel, ParserModel, ToolModel]]  = Field(list(), title="List of Injectable names or injectable dicts called before this phase object is communicated.", description="List of names of Resources, Conditions, Parsers or Tools to run before the target narration object in this phase.", examples=["Condition.C1", "Parser.P1", "Tool.t1"])
    after: List[Union[str, ResourceModel, ConditionModel, ParserModel, ToolModel]]  = Field(list(), title="List of Injectable names or injectable dicts called after this phase object is communicated.",  description="List of names of Resources, Conditions, Parsers or Tools to run after the target narration object in this phase.", examples=["Resource.R1", "Condition.C1", "Parser.P1", "Tool.t1"])

class StagedFixtureModel(FixtureModel, StagedResourcesModel):
    pass