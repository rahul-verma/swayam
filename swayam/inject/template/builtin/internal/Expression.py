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

from .Repeater import RepeaterModel
from .Frame import ExpressionFrameModel

class ExpressionModel(ExpressionFrameModel):
    prompts: List[Union[str, RepeaterModel]] = Field(..., description="Prompt definition names that are included in this expression. Instead of a name it can be dictionary of a RepeatedDefinition.")
    purpose: Union[str,None] = Field(None, description="A statement describing the purpose of the expression.")
    persona: str = Field(None, description="Persona of the expression.")
    directive: str = Field(None, description="Directive text for the narrative this expression builds. Extends previous directives if any.")
    image: Union[str,None] = Field(None, description="Full or Project Relative Path of the image file. Used for the first prompt in the expression and hence becomes a part of the narrative.", examples=["/home/user/abc.png", "user/file.jpeg"])
    out_template: Union[str, None] = Field(None, description="Common output template for all prompts that don't have an output structure of their own")
    draft: Union[str, None] = Field(None, description="Draft name.")
    actions: List[str] = Field([],description="List of actions to be used in the prompts that don't have an action list of their own.")
    
Expression = Template.build("Expression", model=ExpressionModel)