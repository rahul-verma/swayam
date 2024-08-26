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
from .parser import TextContentParser, JsonContentParser, StructuredParser
from .error import *

class Parser(metaclass=ParserMeta):
    
    @classmethod
    def text(cls, name, *, kallable, output_structure):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.
        
        Input structure is assumed to be a string.

        :param name: Name of the parser
        """
        if not callable(kallable):
            raise ParserArgIsNotCallableError(name, kallable=kallable)
        return TextContentParser(name, kallable=kallable, output_structure=output_structure)
    
    @classmethod
    def json(cls, name, *, kallable, content_structure, output_structure):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.
        
        Input structure is assumed to be a string.

        :param name: Name of the parser
        """
        if not callable(kallable):
            raise ParserArgIsNotCallableError(name, kallable=kallable)
        return JsonContentParser(name, kallable=kallable, content_structure=content_structure, output_structure=output_structure)
        