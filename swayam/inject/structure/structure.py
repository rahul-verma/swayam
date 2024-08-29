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
from enum import Enum
from typing import *
from swayam.inject.error import *

from pydantic import BaseModel, ValidationError

from .error import *

class IOStructureObject:
    
    def __init__(self, structure, instance):
        self.__structure = structure
        self.__model_instance = instance
        
    @property
    def structure(self):
        return self.__structure
        
    @property
    def data_model(self):
        return self.__structure.data_model
    
    @property
    def model_instance(self):
        return self.__model_instance
        
    def as_dict(self):
        return self.__model_instance.model_dump()


# Define a base class `Structure` that inherits from `BaseModel`
class IOStructure:
    
    def __init__(self, name, model:BaseModel):
        self.__name = name
        self.__data_model = model
        
    @property
    def type(self):
        return "Structure"
        
    @property
    def name(self):
        return self.__name
        
    @property
    def data_model(self):
        return self.__data_model
    
    @property
    def keys(self):
        return self.__data_model.model_fields.keys()

    @property
    def definition(self):
        data_schema = self.data_model.model_json_schema()
        for _, property in data_schema["properties"].items():
            property.pop("title")
            if "enum" in property:
                property.pop("default")
        return data_schema
    
    def __call__(self, **fields):
        try:
            data_object = self.__data_model(**fields)
            return IOStructureObject(self, data_object)
        except ValidationError as e:
            raise StructureValidationError(
                self, 
                provided_input=fields, 
                error=e
            )