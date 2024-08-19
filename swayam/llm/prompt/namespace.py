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
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_prompt_from_content(cls, role, name, content):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        from swayam import Tool, Structure
        text = None
        purpose = None
        image = None
        output_structure = None
        tools = None
        if type(content) is str:
            text = content
            purpose = cls._create_purpose_from_file_name(name)
        elif type(content) is dict:
            if "text" not in content:
                raise ValueError(f"Prompt file {name} does not contain a text key")  
            else:
                text = content["text"]
            if "purpose" in content:
                purpose = content["purpose"].strip()
            else:
                purpose = cls._create_purpose_from_file_name(name)
            if "image" in content:
                image = content["image"]
            if "output_structure" in content:
                output_structure = content["output_structure"].strip()
                if output_structure:
                    output_structure = getattr(Structure, output_structure)
                   
            if "tools" in content:
                tools_content = content["tools"]
                for tool in tools_content:
                    tool = tool.strip()
                    if tool:
                        if not tools:
                            tools = []
                        tools.append(getattr(Tool, tool))

        from swayam import Prompt
        from swayam.llm.prompt.types import SystemPrompt
        if role == "user":
            return Prompt.text(text, purpose=purpose, image=image, output_structure=output_structure, tools=tools, role=role)
        else:
            return SystemPrompt(text=text)
        
    def __getattr__(self, name):
        role = self.__dict__["_role"]
        from tarkash import YamlFile        
        file = YamlFile(PromptDir.get_path_for_prompt(role=role, name=name))
        return PromptDir.create_prompt_from_content(role, name, file.content)

class UserPromptDir(PromptDir):
    
    def __init__(self):
        super().__init__(role="user")
        
class SystemPromptDir(PromptDir):
    
    def __init__(self):
        super().__init__(role="system")
        
        