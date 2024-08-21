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
from pydantic import BaseModel
from swayam import Structure

class LLMTool:
    
    def __init__(self, name, *, target, desc, input_structure, output_structure, atomic=True):
        self.__name = name
        self.__target = target
        self.__target.__name__ = self.__target.__name__
        self.__desc = desc
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        self.__atomic = atomic
        
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
    def is_atomic(self):
        return self.__atomic
    
    @property
    def definition(self):
        data_schema = self.__input_structure.definition
        schema = {
            "type": "function",
            "function":{
                "name": self.__name,
                "description": self.__desc,
                "parameters": data_schema
            }}
        return schema
    
    @classmethod
    def call_tool_compatible_callable(cls, *, kallable, input_structure, output_structure, atomic=False, **kwargs):
        structure = input_structure(**kwargs)
        from swayam.llm.structure.structure import IOStructureObject
        
        output = kallable(**structure.as_dict())
        
        if atomic:
            if type(output) not in (dict, IOStructureObject):
                raise TypeError("The return value of an atomic tool function must be a dictionary or a Structure object.")
            if not isinstance(output, IOStructureObject):
                return output_structure(**output).as_dict()
            else:
                return output.as_dict()
        else:
            if type(output) is not list:
                raise TypeError("The return value of a non-atomic tool function, generator-compatible function must be a list.")
            updated_output = []
            for item in output:
                if not isinstance(item, IOStructureObject):
                    updated_output.append(output_structure(**item).as_dict())
                else:
                    updated_output.append(item.as_dict())
            
            result = updated_output
            return result
    
    def __call__(self, **kwargs):
        from .response import ToolResponse
        result = LLMTool.call_tool_compatible_callable(kallable=self.__target, input_structure=self.__input_structure, output_structure=self.__output_structure, atomic=self.__atomic, **kwargs)
            
        return ToolResponse(self, result)
        
    def as_generator(self, name=None):
        if name is None:
            name = self.__name + "_Generator"
        from swayam.llm.generator.generator import MapGeneratorCreator
        return MapGeneratorCreator(name, data_object=self.__target, input_structure=self.__input_structure, output_structure=self.__output_structure, from_tool=True)