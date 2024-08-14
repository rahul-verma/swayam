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

from pydantic import BaseModel, Field
from enum import Enum
from typing import *

from .structure import create_structure
import json

class Tool:
    
    def __init__(self, target, desc, tool_structure):
        self.__name = target.__name__
        self.__target = target
        self.__desc = desc
        self.__tool_structure = tool_structure
        
    @property
    def name(self):
        return self.__name
    
    @property
    def qname(self):
        return self.__target.__module__ + "." + self.__name
    
    @property
    def desc(self):
        return self.__desc
    
    @property
    def definition(self):
        data_schema = json.loads(self.__tool_structure.schema_json())
        data_schema.pop("title")
        for _, property in data_schema["properties"].items():
            if "enum" in property:
                property.pop("title")
                property.pop("default")
        schema = {
            "type": "function",
            "function":{
                "name": self.__name,
                "description": self.__desc,
                "parameters": data_schema
            }}
        return schema
    
    def __call__(self, **fields):
        structure = self.__tool_structure(**fields)
        return self.__target(**structure.dict())
    
    
class ToolBuilder:
    def __init__(self, target:callable, desc:str):
        self.__target = target
        self.__tool_name = target.__name__
        self.__fields = {}
        self.__desc = desc
        
    def add_field(self, name:str, *, type, desc:str, default="not_given"):
        is_enum = False
        try:
            is_enum = issubclass(type, Enum)
        except TypeError:
            pass
        
        if is_enum:
            choices = [entry.value for entry in type]
            if isinstance(default, Enum):
                default = default.name
            return self.add_choices(name, choices=choices, desc=desc, default=default)
        if default=="not_given":
            self.__fields[name] = (type, Field(..., description=desc))
        else:
            self.__fields[name] = (type, Field(default, description=desc))
            
    def add_choices(self, name:str, *, choices, desc:str, default="not_given"):
        type_def = Literal.__getitem__(tuple(choices))
        self.add_field(name, type=type_def, desc=desc, default=default)
        
    def build(self):
        return Tool(self.__target, self.__desc, create_structure(self.__tool_name + "_arguments", **self.__fields))