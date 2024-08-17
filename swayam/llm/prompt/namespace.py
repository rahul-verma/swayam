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
        
    def __getattr__(self, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        from swayam.core.constant import SwayamOption
        self.__base_path = os.path.join(Tarkash.get_option_value(SwayamOption.PROMPT_ROOT_DIR), self.__dict__["_role"])

        file = YamlFile(os.path.join(self.__base_path, f"{name}.yaml"))
        
        text = None
        image = None
        response_format = None
        tools = None
        
        content = file.content
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
                    project_name = Tarkash.get_option_value(SwayamOption.PROJECT_NAME)
                    structure_module = importlib.import_module(f"{project_name}.lib.hook.structure")
                    response_format = getattr(structure_module, response_format)
            if "tools" in content:
                tools_content = content["tools"]
                for tool in tools_content:
                    tool = tool.strip()
                    if tool:
                        project_name = Tarkash.get_option_value(SwayamOption.PROJECT_NAME)
                        tool_module = importlib.import_module(f"{project_name}.lib.hook.tool")
                        if tools is None:
                            tools = []
                        tools.append(getattr(tool_module, tool))

        from swayam import Prompt
        return Prompt.user_prompt(text, image=image, response_format=response_format, tools=tools)
        

class UserPromptDir(PromptDir):
    
    def __init__(self):
        super().__init__(role="user")
        
class SystemPromptDir(PromptDir):
    
    def __init__(self):
        super().__init__(role="system")
        
        