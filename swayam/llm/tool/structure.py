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

from pydantic import BaseModel, create_model, Field
from enum import Enum
from typing import *

class StructureBuilder:
    def __init__(self, name:str):
        self.__name = name
        self.__fields = {}
        
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
        # Define a base class `Structure` that inherits from `BaseModel`
        class Structure(BaseModel):
            pass

        from swayam.llm.tool import Tool
        model_fields = {name: (field_type, field_info) for name, (field_type, field_info) in self.__fields.items()}
        
        return create_model(self.__name, __base__=BaseModel, **model_fields)