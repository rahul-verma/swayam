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

from .meta import ParserMeta
from .parser import TextContentParser, JsonContentParser
from .error import *

kallable = callable

class Parser(metaclass=ParserMeta):
    
    @classmethod
    def text(cls, name, *, callable, output_structure=None, input_structure=None, allow_none_output=False):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.
        
        Input structure is assumed to be a string.

        :param name: Name of the parser
        """
        return TextContentParser(name, 
                                 callable=callable, 
                                 input_structure=input_structure,
                                 output_structure=output_structure,
                                 allow_none_output=allow_none_output)
    
    @classmethod
    def json(cls, name, *, callable, output_structure, input_structure=None, schema_validator=None, allow_none_output=False):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.
        
        Input structure is assumed to be a string.

        :param name: Name of the parser
        """
        return JsonContentParser(name, callable=callable, input_structure=input_structure, output_structure=output_structure, allow_none_output=allow_none_output, schema_validator=schema_validator)
        