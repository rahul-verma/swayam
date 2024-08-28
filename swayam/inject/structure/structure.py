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
from .error import *

from pydantic import BaseModel, ValidationError

class IOStructureObject:
    
    def __init__(self, structure, instance):
        self.__structure = structure
        self.__model_instance = instance
        
    @property
    def struct_name(self):
        return self.__structure.name
        
    @property
    def data_model(self):
        return self.__structure.data_model
    
    @property
    def model_instance(self):
        return self.__model_instance
        
    def as_dict(self):
        return self.__model_instance.model_dump()
    
class IOStructureObjectList:
    def __init__(self, structure, *items):
        self.__structure = structure
        self.__instances = self.__structure.data_model(items=list(items)).items      
        
    @property
    def struct_name(self):
        return self.__structure.name 
        
    def append(self, item):
        if not isinstance(item, IOStructureObject):
            raise ValueError("Item must be of type IOStructureObject")

        items_field_type = self.__structure.data_model.__annotations__['items']
        item_model_type = get_args(items_field_type)[0]
        if item.data_model != item_model_type:
            raise ValueError(f"Wrong DataModel in the object. Expected {item_model_type}. Got: {item.data_model}")
        self.__instances.append(item.model_instance)
        
    def as_list(self):
        return [instance.model_dump() for instance in self.__instances]
    
    def __iter__(self):
        return iter(self.__instances)


# Define a base class `Structure` that inherits from `BaseModel`
class IOStructure:
    
    def __init__(self, name, model:BaseModel, composite_structure=None):
        self.__name = name
        self.__data_model = model
        self.__composite_structure = composite_structure
        
    @property
    def name(self):
        return self.__name
        
    @property
    def data_model(self):
        return self.__data_model

    def is_atomic(self):
        return True
    @property
    def composite_structure(self):
        return self.__composite_structure

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
            raise StructureValidationError(self.__name, message=f"Invalid data: {e}")

class IOStructureList:
    
    def __init__(self, name, atomic_model:BaseModel, composite_model:BaseModel):
        self.__name = name
        self.__atomic_model = atomic_model
        self.__composite_model = composite_model
        
    @property
    def name(self):
        return self.__name
    @property
    def atomic_model(self):
        return self.__data_model
    
    @property
    def data_model(self):
        return self.__composite_model
    
    def is_atomic(self):
        return False

    @property
    def definition(self):
        data_schema = self.data_model.model_json_schema()
        for _, property in data_schema["properties"].items():
            property.pop("title")
            if "enum" in property:
                property.pop("default")
        return data_schema
    
    def __call__(self, *items):
        return IOStructureObjectList(self, *items)