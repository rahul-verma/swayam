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
from swayam.inject.structure.structure import IOStructureObject

class StructuredParser:
    
    def __init__(self, name, *, callable, input_structure, output_structure):
        self.__name = name
        self.__callable = callable
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        self.__request = None
        
    @property
    def request(self):
        return self.__request
    
    @request.setter
    def request(self, request):
        self.__request = request
 
    def __call__(self, **kwargs):
        from swayam.inject.tool.tool import StructuredTool
    
        output_iterable = None

        args = self.__input_structure(**kwargs).as_dict()
        output = self.__callable(**args)
        
        if isinstance(output, IOStructureObject):
            output = output.as_dict()
        else:
            if self.__output_structure.is_atomic():
                output = self.__output_structure(**output).as_dict()
            else:
                output = self.__output_structure(**output).as_list()
        
        self.request.append_parser_output(output)
        return output

        