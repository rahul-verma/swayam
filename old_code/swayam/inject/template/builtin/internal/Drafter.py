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

from typing import Union, List, Literal
from pydantic import BaseModel, Field

from swayam import Template

from .FrameInjectable import InjectableModel

class ReferenceDependencyModel(BaseModel):
    name: str = Field(..., description="Name of the reference.")
    iter_content: bool = Field(False, description="Whether to iterate over the contents of the reference.")
    
class DrafterDefinitionModel(BaseModel):
    definitions: List[str] = Field(..., description="Children Definition names to be repeated.")
    entity: str = Field(..., description="Name of the entity to draft a fragment")
    aggregate_name: str = Field(..., description="Name of the aggregate. If None, it is same as the plural name for the entities.")
    interim: bool = Field(True, description="Whether this aggregate is an interim draft. In such a case, it is local to the current thought and not stored in blueprints as reference for other thoughts.")
    blueprint_name: Union[str,None] = Field(None, description="Name of the blueprint to export the aggregate. If not provided, it is stored as the name of the aggregate. A prefix 'generated_' is added to the name of the aggregate in both the cases.")
    mode: Literal["overwrite", "append"] = Field("overwrite", description="Mode of drafting.")
    reset_conversation: bool = Field(True, description="Whether conversation is reset for the repeated prompts or not.")
    refer: List[Union[str, ReferenceDependencyModel]] = Field(list(), description="List of references that this draft depends on.")
    feed: List[Union[str,InjectableModel]] = Field(list(), description="List of references that this draft depends on.")
    force_unique_entries: bool = Field(False, description="If True, it forces creation of additional primary keys if content for primary key already exists. Default is False.")
    
class DraftModel(BaseModel):
    draft: DrafterDefinitionModel = Field(..., description="Draft dictionary.")

DrafterTemplate = Template.build("DrafterTemplate", model=DrafterDefinitionModel)    
DraftTemplate = Template.build("DraftTemplate", model=DraftModel)