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
from swayam.inject.injectable import Injectable

from pydantic import BaseModel, ValidationError

from .error import *

class Data(Injectable):
    
    def __init__(self, template, instance):
        self.__template = template
        self.__model_instance = instance
        
    @property
    def name(self):
        return self.__template.name
        
    @property
    def template(self):
        return self.__template
        
    @property
    def model(self):
        return self.__template.model
    
    @property
    def model_instance(self):
        return self.__model_instance
        
    def as_dict(self):
        return self.__model_instance.model_dump()
    
    def __getattr__(self, key):
        if key in self.template.keys:
                return getattr(self.__model_instance, key)
        else:
            raise DataAttributeDoesNotExistError(self, attribute=key)
        
    __getitem__ = __getattr__


# Define a base class `Structure` that inherits from `BaseModel`
class DataTemplate(Injectable):
    
    def __init__(self, name, description, model:BaseModel, plural=False, plural_key=None, base_model=None):
        super().__init__(type="Template", name=name)
        self.__description = description
        self.__model = model
        self.__plural = plural
        self.__plural_key = plural_key
        self.__base_model = base_model
        
        if self.__description is None:
            self.__description = self.name
        
    @property
    def model(self):
        return self.__model
    
    @property
    def is_plural(self):
        return self.__plural
    
    @property
    def plural_key(self):
        return self.__plural_key
    
    @property
    def base_model(self):
        return self.__base_model
    
    @property
    def description(self):
        return self.__description
    
    @property
    def keys(self):
        return self.__model.model_fields.keys()

    @property
    def definition(self):
        def remove_title_key(data):
            if isinstance(data, dict):
                # Remove 'title' key if it exists at the current level
                if 'title' in data:
                    del data['title']
                
                # Recursively remove 'title' from nested dictionaries
                for key, value in list(data.items()):
                    remove_title_key(value)
            
            elif isinstance(data, list):
                # If it's a list, iterate through all elements and remove 'title' from each
                for item in data:
                    remove_title_key(item)
        data_schema = self.model.model_json_schema()
        remove_title_key(data_schema)
        # for _, property in data_schema["properties"].items():
        #     if "title" in property:
        #         property.pop("title")
        #     if "enum" in property:
        #         property.pop("default")
        return data_schema
    
    def __call__(self, **fields):
        try:
            data_object = self.__model(**fields)
            return Data(self, data_object)
        except ValidationError as e:
            raise TemplateValidationError(
                self, 
                provided_input=fields, 
                error=e
            )