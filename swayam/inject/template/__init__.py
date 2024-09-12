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
from .meta import TemplateMeta
from .template import DataTemplate

class Template(metaclass=TemplateMeta):
    
    @classmethod
    def build(cls, name, model:BaseModel):
        """
        Create a dynamic Pydantic BaseModel class inheriting from a given base class.

        args:
            name(str): Name of the structure
            model(BaseModel): The encapsulated Pydantic Data Model
        """
        return DataTemplate(name, model=model)
        