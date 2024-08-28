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

from pydantic import BaseModel
from .meta import GeneratorMeta

kallable = callable

class Generator(metaclass=GeneratorMeta):
    
    @classmethod
    def data(cls, name, *, data, io_structure):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the structure
        """
        from .generator import StructuredGeneratorCreator
        return StructuredGeneratorCreator(name, data_object=data, input_structure=io_structure.composite_structure, output_structure=io_structure)
    
    @classmethod
    def callable(cls, name, *, callable, input_structure, output_structure):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the structure
        """
        from .generator import StructuredGeneratorCreator
        if not jcallable(callable):
            raise ValueError("Expected a callable object.")
        return StructuredGeneratorCreator(name, data_object=callable, input_structure=input_structure, output_structure=output_structure)
    
    def tool(self, *, tool, name=None):
        if name is None:
            name = tool.name + "_Generator"
        from .generator import StructuredGeneratorCreator
        return StructuredGeneratorCreator(name, data_object=tool.target, input_structure=tool.input_structure, output_structure=tool.output_structure)
        