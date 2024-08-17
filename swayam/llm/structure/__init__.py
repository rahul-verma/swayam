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

import importlib

class Structure:
    
    @classmethod
    def builder(cls, name:str):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the structure
        """
        from .builder import StructureBuilder
        return StructureBuilder(name)
    
    @classmethod
    def import_structure(self, name:str):
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        project_name = Tarkash.get_option_value(SwayamOption.PROJECT_NAME)
        structure_module = importlib.import_module(f"{project_name}.lib.hook.structure")
        return getattr(structure_module, name)