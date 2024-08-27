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

class StructuredTool:
    
    def __init__(self, name, *, target, description, input_structure, output_structure, none_text:str):
        self.__name = name
        self.__target = target
        self.__target.__name__ = self.__target.__name__
        self.__description = description
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        self.__none_text = none_text
        
    @property
    def name(self):
        return self.__name
    
    @property
    def target_name(self):
        return self.__target.__name__
    
    @property
    def target(self):
        return self.__target
    
    @property
    def input_structure(self):
        return self.__input_structure
    
    @property
    def output_structure(self):
        return self.__output_structure
    
    @property
    def description(self):
        return self.__description
    
    @property
    def definition(self):
        data_schema = self.__input_structure.definition
        schema = {
            "type": "function",
            "function":{
                "name": self.__name,
                "description": self.__description,
                "parameters": data_schema
            }}
        return schema
    
    @classmethod
    def call_tool_compatible_callable(cls, *, kallable, input_structure, output_structure,  none_text, **kwargs):
        structure = input_structure(**kwargs)
        from swayam.inject.structure.structure import IOStructureObject, IOStructureObjectList
        
        output = kallable(**structure.as_dict())
        
        if output_structure.is_atomic():
            if type(output) not in (dict, IOStructureObject):
                raise TypeError("The return value of an atomic tool function must be a dictionary or a Structure object.")
            if not isinstance(output, IOStructureObject):
                return output_structure(**output).as_dict()
            else:
                return output.as_dict()
        else:
            if type(output) not in (list, IOStructureObjectList):
                raise TypeError("The return value of a non-atomic tool function, generator-compatible function must be a list or IOStructureObjectList.")
            if not isinstance(output, IOStructureObjectList):
                return output_structure(*output).as_list()
            else:
                return output.as_list()
    
    def __call__(self, **kwargs):
        from .response import ToolResponse
        result = StructuredTool.call_tool_compatible_callable(kallable=self.__target, input_structure=self.__input_structure, output_structure=self.__output_structure, none_text=self.__none_text, **kwargs)
            
        return ToolResponse(self, result)