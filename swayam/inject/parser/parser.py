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
from json import JSONDecodeError
from enum import Enum
from typing import *

from pydantic import BaseModel, create_model, Field
from swayam.inject.structure.structure import IOStructureObject, IOStructureObjectList
from swayam.inject.structure.error import StructureValidationError

from .error import *

class StructuredParser:
    
    def __init__(self, name, *, kallable, output_structure, content_structure=None):
        self.__name = name
        self.__kallable = kallable
        self.__content_structure = content_structure
        self.__output_structure = output_structure
        self.__prompt = None
        
    @property
    def name(self):
        return self.__name
        
    @property
    def _content_structure(self):
        return self.__content_structure
 
    def __call__(self, *, content):
        from swayam.inject.tool.tool import StructuredTool
    
        output_iterable = None

        if self.__content_structure is not None:
            if self.__content_structure.is_atomic():
                input_to_callable = self.__content_structure(**content).as_dict()
            else:
                input_to_callable = self.__content_structure(*content).as_list()
        else:
            input_to_callable = content

        output = self.__kallable(content=input_to_callable)
        
        if isinstance(output, IOStructureObject):
            output = output.as_dict()
        elif isinstance(output, IOStructureObjectList):
            output = output.as_list()
        else:
            if self.__output_structure.is_atomic():
                output = self.__output_structure(**output).as_dict()
            else:
                output = self.__output_structure(**output).as_list()

        return output


class TextContentParser(StructuredParser):
    
    def __init__(self, name, *, kallable, output_structure):
        super().__init__(name, kallable=kallable, output_structure=output_structure)
        
class JsonContentParser(StructuredParser):
    
    def __init__(self, name, *, kallable, content_structure, output_structure):
        super().__init__(name, kallable=kallable, content_structure=content_structure, output_structure=output_structure)

    def __call__(self, *, content):
        if not isinstance(content, str):
            raise ParserCallError(self.name, f"Expected 'content' argument as a string. Got: {content} of type {type(content)}")
        try:
            content = json.loads(content)
        except JSONDecodeError as e:
            raise ParserCallError(f'Invalid JSON content: {e}')
        
        return super().__call__(content=content)
