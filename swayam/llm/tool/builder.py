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
import json

class ToolBuilder:
    def __init__(self, target:callable, desc:str):
        self.__target = target
        self.__tool_name = target.__name__
        self.__desc = desc
        from ..structure.builder import StructureBuilder
        self.__structure_builder = StructureBuilder(self.__tool_name + "_arguments")
        
    def add_field(self, name:str, *, type, desc:str, default="not_given"):
        self.__structure_builder.add_field(name, type=type, desc=desc, default=default)
            
    def add_choices(self, name:str, *, choices, desc:str, default="not_given"):
        self.__structure_builder.add_choices(name, choices=choices, desc=desc, default=default)
        
    def build(self):
        from swayam.llm.tool import Tool
        return Tool(self.__target, self.__desc, self.__structure_builder.build())