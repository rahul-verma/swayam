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

from typing import List

from pydantic import BaseModel, create_model, field_validator, Field
from .meta import StructureMeta

class Structure(metaclass=StructureMeta):
    
    @classmethod
    def build(cls, name, model:BaseModel, return_composite=False):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        :param name: Name of the structure
        """
        
        def create_list_model(input_model):
            # def ensure_list(cls, v):
            #     if not isinstance(v, list):
            #         return [v]
            #     return v

            # Create the dynamic model with the validator attached
            ListModel = create_model(
                f'{input_model.__name__}List',
                items=(List[input_model], Field(default_factory=list)),
                # __validators__={
                #     'items': field_validator('items', mode='before')(ensure_list)
                # }
            )
            
            return ListModel
        
        from .structure import IOStructure, IOStructureList
        
        # Generators derive the list model automatically. So, a composite structure is always created.
        atomic_model = model
        composite_model = create_list_model(model)
        composite_structure = IOStructureList(f'{name}List', atomic_model=atomic_model, composite_model=composite_model)
        atomic_structure = IOStructure(name, model, composite_structure)
        
        if return_composite:
            return atomic_structure, composite_structure
        else:
            return atomic_structure
        