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
from .namespace import UserPromptDir, SystemPromptDir
from swayam.llm.structure.structure import ResponseStructure

class Prompt:
    user = UserPromptDir()
    system = SystemPromptDir()
    
    @classmethod
    def user_prompt(cls, text, *, purpose:str=None, image:str=None, response_format:Union[str, ResponseStructure]=None, tools:list=None) -> UserPrompt:
        from swayam import Tool, Structure
        if response_format is not None and type(response_format) is str:
            response_format = Structure.import_structure(response_format)
        if tools is not None:
            output_tools = []
            for tool in tools:
                if type(tool) is str:
                    output_tools.append(Tool.import_tool(tool))
                else:
                    output_tools.append(tool)
            tools = output_tools
                
        return UserPrompt(text=text, purpose=purpose, image=image, response_format=response_format, tools=tools)