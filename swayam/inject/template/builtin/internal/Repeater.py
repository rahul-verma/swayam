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

from swayam import Template

from .FrameInjectable import FrameInjectableModel
    
class RepeatedExpressionDefinitionsModel(BaseModel):
    definitions: List[str] = Field(..., title="Children Definition names", description="Children Definition names to be repeated.")
    driver: Union[FrameInjectableModel, str] = Field(..., title="Driver", description="Driver to be used for repeating the children phases.")
    
class RepeatedPromptDefinitionsModel(RepeatedExpressionDefinitionsModel):
    definitions: List[str] = Field(..., title="Children Definition names", description="Children Definition names to be repeated.")
    driver: Union[FrameInjectableModel, str] = Field(..., title="Driver", description="Driver to be used for repeating the children phases.")
    standalone: bool = Field(False, title="Standalone", description="Whether the repeated prompts are standalone or not.")
    
class PromptRepeaterModel(BaseModel):
    repeat: RepeatedPromptDefinitionsModel = Field(..., title="Prompt Repeater Definition", description="Repeater dictionary.")
    
class ExpressionRepeaterModel(BaseModel):
    repeat: RepeatedExpressionDefinitionsModel = Field(..., title="Expression Repeater Definition", description="Repeater dictionary.")