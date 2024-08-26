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
from .parser import StructuredParser
from .error import ParserArgIsNotCallableError
from swayam.inject.structure.builtin import BoolOutput

class Parser(metaclass=ParserMeta):
    
    @classmethod
    def callable(cls, name, *, kallable, input_structure, output_structure):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the parser
        """
        if not callable(kallable):
            raise ParserArgIsNotCallableError(name, kallable=kallable)
        return StructuredParser(name, kallable=kallable, input_structure=input_structure, output_structure=output_structure)
    
    def tool(self, *, tool, name=None):
        if name is None:
            name = tool.name + "_Parser"
        return StructuredParser(name, data_object=tool.target, input_structure=tool.input_structure, output_structure=tool.output_structure)
        