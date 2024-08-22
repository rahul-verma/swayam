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
from enum import Enum
from typing import *

from pydantic import BaseModel, create_model, Field


# Define a base class `Structure` that inherits from `BaseModel`

def iterator(name, *, data_object, input_structure, output_structure, from_tool=False, **data_object_kwargs):
    from swayam.tool.tool import StructuredTool
    
    if from_tool:
        data_object = StructuredTool.call_tool_compatible_callable(kallable=data_object, input_structure=input_structure, output_structure=output_structure, **data_object_kwargs)
    elif callable(data_object):
        call_structure = input_structure(**data_object_kwargs)
        data_object = data_object(**call_structure.as_dict())
    for data in data_object:
        yield data
        
class StructuredGenerator:
    
    def __init__(self, name, *, data_object, input_structure, output_structure, from_tool=False, **data_object_kwargs):
        self.__name = name
        self.__data_object = data_object
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        self.__from_tool = from_tool
        self.__data_object_kwargs = data_object_kwargs
 
    def __iter__(self):
        return iterator(self.__name, data_object=self.__data_object, input_structure=self.__input_structure, output_structure=self.__output_structure, from_tool=self.__from_tool, **self.__data_object_kwargs)

class StructuredGeneratorCreator:
    
    def __init__(self, name, *, data_object, input_structure, output_structure, from_tool=False):
        self.__name = name
        self.__data_object = data_object
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        self.__from_tool = from_tool
 
    def __call__(self, **kwargs):
        return StructuredGenerator(self.__name, data_object=self.__data_object, input_structure=self.__input_structure, output_structure=self.__output_structure, from_tool=self.__from_tool, **kwargs)
