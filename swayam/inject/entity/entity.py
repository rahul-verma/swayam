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
    
import os, json

from copy import deepcopy
from typing import Any

from abc import ABC, abstractmethod
from swayam.inject.template.template import DataTemplate


class Entity:
    
    def __init__(self, *, name, singular_name=None, plural_name=None, description=None, template=None, template_primary_key=None, refer=None, feed=None, interim=False, export_as=None) -> None:
        self.__name = name
        self.__file_name = name + ".json"
        self.__singular_name = singular_name
        self.__plural_name = plural_name
        self.__description = description
        self.__template_name = template
        if self.__template_name is None:
            self.__template_name = "TextContent"
        self.__template_primary_key = template_primary_key
        
        from swayam import Template
        template = getattr(Template, self.__template_name)
        
        if self.__singular_name is None:
            self.__singular_name = name
        if self.__plural_name is None:
            self.__plural_name = self.__singular_name + "s"
        if self.__description is None:
            self.__description = template.description
        self.__primary_key = self.__template_primary_key
        if self.__primary_key is None:
            self.__primary_key = name + "_name"
        self.__content_key = name + "_content"
        
        from pydantic import create_model, Field
        field_defs = {}
        field_defs[self.__primary_key] = (str, Field(..., description="Name of the " + self.__singular_name))
        field_defs[self.__content_key] = (template.model, Field(..., description="Data Content for " + self.__description))
        model = create_model(template.name + "FragmentModel", **field_defs)
        self.__template = Template.build(template.name + "Fragment", description=self.__description.title(), model=model)
        self.__description = self.__template.description.title()
                
    @property
    def name(self):
        return self.__name
    
    @property
    def file_name(self):
        return self.__file_name
    
    @property
    def singular_name(self):
        return self.__singular_name
    
    @property
    def plural_name(self):
        return self.__plural_name
                
    @property
    def description(self):
        return self.__description
    
    @property
    def template_name(self):
        return self.__template_name
    
    @property
    def template(self):
        return self.__template
    
    @property
    def template_primary_key(self):
        return self.__template_primary_key
    
    @property
    def primary_key(self):
        return self.__primary_key
    
    @property
    def content_key(self):
        return self.__content_key