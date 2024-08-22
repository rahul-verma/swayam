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

from pydantic import BaseModel

class IOStructureObject:
    
    def __init__(self, structure, instance):
        self.__structure = structure
        self.__model_instance = instance
        
    def as_dict(self):
        print(self.__model_instance)
        return self.__model_instance.model_dump()
    
class IOStructureObjectList:
    def __init__(self, structure, *items):
        self.__structure = structure
        self.__instances = self.__structure.data_model(items=items).items
        self.__structures = [IOStructureObject(structure, item) for item in self.__instances]
        
    def as_list(self):
        return [structure.as_dict() for structure in self.__structures]


# Define a base class `Structure` that inherits from `BaseModel`
class IOStructure:
    
    def __init__(self, name, model:BaseModel):
        self.__name__ = name
        self.__data_model = model
        
    @property
    def data_model(self):
        return self.__data_model

    @property
    def definition(self):
        data_schema = self.data_model.model_json_schema()
        for _, property in data_schema["properties"].items():
            property.pop("title")
            if "enum" in property:
                property.pop("default")
        return data_schema
    
    def __call__(self, **fields):
        return IOStructureObject(self, self.__data_model(**fields))
    

class IOStructureList:
    
    def __init__(self, name, model:BaseModel):
        self.__name__ = name
        self.__data_model = model
        
    @property
    def data_model(self):
        return self.__data_model

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