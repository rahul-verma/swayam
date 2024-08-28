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

from .error import *

class StructuredTool:
    
    def __init__(self, name, *, callable, description, input_structure, output_structure):
        self.__name = name
        self.__callable = callable
        self.__callable_name = self.__callable.__name__
        self.__description = description
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        from swayam.inject import Injectable
        Injectable.validate_callable_definition(self)
        
    @property
    def name(self):
        return self.__name
    
    @property
    def callable_name(self):
        return self.__callable_name
    
    @property
    def callable(self):
        return self.__callable
    
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
    
    def __call__(self, **kwargs):
        from .response import ToolResponse
        
        
        output = callable(**structure.as_dict())
        
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