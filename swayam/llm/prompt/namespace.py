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

import os
import importlib
from abc import ABC, abstractmethod


class PromptDir(ABC):   
    
    def __init__(self, *, role):
        self._role = role
        
    @classmethod
    def get_path_for_prompt(cls, *, role, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        return os.path.join(Tarkash.get_option_value(SwayamOption.PROMPT_ROOT_DIR), role, f"{name}.yaml")
        
    @classmethod
    def create_prompt_from_content(cls, content):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        from swayam import Tool, Structure
        text = None
        image = None
        response_format = None
        tools = None
        if type(content) is str:
            text = content
        elif type(content) is dict:
            if "prompt" not in content:
                raise ValueError(f"Prompt file {name} does not contain a prompt key")  
            else:
                text = content["prompt"]
            if "image" in content:
                image = content["image"]
            if "response_format" in content:
                response_format = content["response_format"].strip()
                if response_format:
                    response_format = Structure.import_structure(response_format)
                   
            if "tools" in content:
                tools_content = content["tools"]
                for tool in tools_content:
                    tool = tool.strip()
                    if tool:
                        if not tools:
                            tools = []
                        tools.append(Tool.import_tool(tool))

        from swayam import Prompt
        return Prompt.user_prompt(text, image=image, response_format=response_format, tools=tools)
        
    def __getattr__(self, name):
        role = self.__dict__["_role"]
        from tarkash import YamlFile        
        if name == "formatter":
            from .format import FormatterMediator
            return FormatterMediator(role=role)

        file = YamlFile(PromptDir.get_path_for_prompt(role=role, name=name))
        return PromptDir.create_prompt_from_content(file.content)
        

class UserPromptDir(PromptDir):
    
    def __init__(self):
        super().__init__(role="user")
        
class SystemPromptDir(PromptDir):
    
    def __init__(self):
        super().__init__(role="system")
        
        