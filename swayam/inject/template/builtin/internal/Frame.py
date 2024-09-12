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
from swayam import Template

from .Cue import CueModel
from .Action import ActionModel
from .Prop import PropModel

class PromptStepsModel(BaseModel):
    prologue_prompt: List[Union[str, PropModel, CueModel, ActionModel]]  = Field(list(), description="List of names or dictionaries of Props, Cues and Actions to run before each of the prompts in this expression.")
    epilogue_prompt: List[Union[str, CueModel, ActionModel]]  = Field(list(), description="List of names or dictionaries of Cues and Actions to run after each of the prompts in this expression.")
    
class FrameModel(BaseModel):
    prologue: List[Union[str, PropModel, CueModel, ActionModel]]  = Field(list(), description="List of names or dictionaries of Props, Cues and Actions to run before the target narration object of this phase.")
    epilogue: List[Union[str, PropModel, CueModel, ActionModel]]  = Field(list(), description="List of names or dictionaries of Cues and Actions to run after the target narration object in this phase.")

class ExpressionFrameModel(FrameModel, PromptStepsModel):
    pass