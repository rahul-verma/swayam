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

class StagedResources(BaseModel):
    once: List[str] = Field(list(), title="Resources created only once for this phase.", description="List of names of Resources to be setup once per this phase, across all the children narration objects.", examples=["R1", "Resources.R1"])
    every: List[str] = Field(list(), title="Resources created for every child in this phase.", description="List of names of Resources to be setup on a per-child=basis.", examples=["R2", "Resources.R2"])
    
class FixtureModel(BaseModel):
    resources: List[str] = Field(list(), title="List of Resource names", description="List of names of resources to be made available.", examples=["Resource.R1", "Resource.R2"])
    before: List[str] = Field(list(), title="List of Injectable names called before this phase object is communicated.", description="List of names of Conditions, Parsers or Tools to run before the target narration object in this phase.", examples=["Condition.C1", "Parser.P1", "Tool.t1"])
    after: List[str] = Field(list(), title="List of Injectable names called after this phase object is communicated.",  description="List of names of Conditions, Parsers or Tools to run after the target narration object in this phase.", examples=["Condition.C1", "Parser.P1", "Tool.t1"])

class StagedFixtureModel(BaseModel):
    resources: StagedResources = Field(StagedResources(), title="Staged Resources Dictionary", description="Staged Resources to be made available.")
    before: List[str] = Field(list(), title="List of Injectable names called before this phase object is communicated.", description="List of names of Conditions, Parsers or Tools to run before the target narration object in this phase.", examples=["Condition.C1", "Parser.P1", "Tool.t1"])
    after: List[str] = Field(list(), title="List of Injectable names called after this phase object is communicated.", description="List of names of Conditions, Parsers or Tools to run after the target narration object in this phase.", examples=["Condition.C1", "Parser.P1", "Tool.t1"])