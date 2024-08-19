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

import json

class LLMTool:
    
    def __init__(self, name, *, target, desc, call_structure):
        self.__name = name
        self.__target = target
        self.__target.__name__ = self.__target.__name__
        self.__desc = desc
        self.__call__structure = call_structure
        
    @property
    def name(self):
        return self.__name
    
    @property
    def target_name(self):
        return self.__target.__name__
    
    @property
    def desc(self):
        return self.__desc
    
    @property
    def definition(self):
        data_schema = self.__call__structure.definition
        schema = {
            "type": "function",
            "function":{
                "name": self.__name,
                "description": self.__desc,
                "parameters": data_schema
            }}
        return schema
    
    def __call__(self, **fields):
        structure = self.__call__structure(**fields)
        from .response import ToolResponse
        output = self.__target(**structure.dict())
        return ToolResponse(self, output)