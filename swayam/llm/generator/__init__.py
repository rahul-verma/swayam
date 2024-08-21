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

class Generator(metaclass=GeneratorMeta):
    
    @classmethod
    def build(cls, name, *, data_object, output_structure):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the structure
        """
        from .generator import MapGeneratorCreator
        return MapGeneratorCreator(name, data_object=data_object, output_structure=output_structure)
    
    @classmethod
    def create_generator_from_content(cls, *, generator, args=None):
        from swayam import Generator
        if args == None:
            args = {}
        return getattr(Generator, generator)(**args)
        