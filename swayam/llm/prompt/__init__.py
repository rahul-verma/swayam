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

from typing import Union

from .types import UserPrompt, SystemPrompt
from swayam.llm.structure.structure import IOStructure
from .format import FormatterMediator
from .meta import PromptMeta

class Prompt(metaclass=PromptMeta):
    
    @classmethod
    def text(cls, text, *, purpose:str=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, role:str="user") -> UserPrompt:
        from swayam import Tool, Structure
        if output_structure is not None and type(output_structure) is str:
            output_structure = getattr(Structure, output_structure)
        if tools is not None:
            output_tools = []
            for tool in tools:
                if type(tool) is str:
                    output_tools.append(getattr(Tool, tool))
                else:
                    output_tools.append(tool)
            tools = output_tools
                
        return UserPrompt(text=text, purpose=purpose, image=image, output_structure=output_structure, tools=tools)
    
    @classmethod
    def formatter(cls, **fmt_kwargs):
        return FormatterMediator(**fmt_kwargs)