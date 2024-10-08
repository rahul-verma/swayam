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
from .Frame import FrameModel

class LLMModel(BaseModel):
    provider: Literal['openai'] = Field(..., description="The provider of the LLM")
    name: str = Field(..., description="Name of the model.")

class PromptModel(FrameModel):
    purpose: Union[str,None] = Field(None, description="A statement describing the purpose of the prompt.")
    text: str = Field(..., description="Text content")
    image: Union[str,None] = Field(None, description="Full or Project Relative Path of the image file. Must include file name.", examples=["/home/user/abc.png", "user/file.jpeg"])
    out_template: Union[str, None] = Field(None, description="Output Template for what the prompt responds with.")
    actions: List[str] = Field([], description="List of actions to be used in the prompt")
    reset_conversation: bool = Field(False,description="If True, it gets an empty narrative value, except for the context message. The follow-up prompts continue with the narrative before it.")
    model: LLMModel = Field(None, description="The model to use for the prompt.")
    
Prompt = Template.build("Prompt", model=PromptModel)