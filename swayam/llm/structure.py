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

from typing import Dict, Type
from pydantic import BaseModel, create_model

# Define a base class `Structure` that inherits from `BaseModel`
class Structure(BaseModel):
    pass

def create_structure(klass_name: str, **fields):
    """
    Create a dynamic Pydantic BaseModel class inheriting from a given base class.

    :param name: The name of the model class.
    :param fields: A dictionary where keys are field names and values are field types.
    :return: A new Pydantic BaseModel subclass with the given name and fields.
    """
    annotations = {field_name: (field_type, ...) for field_name, field_type in fields.items()}
    
    return create_model(klass_name, __base__=Structure, **annotations)