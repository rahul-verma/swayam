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


class Artifact:
    
    def __init__(self, *, name, singular_name=None, plural_name=None, description=None, template=None, refer=None, feed=None, interim=False, store_as=None) -> None:
        self.__name = name
        self.__singular_name = singular_name
        self.__plural_name = plural_name
        self.__description = description
        self.__template_name = template
        if self.__template_name is None:
            self.__template_name = "TextContent"
        self.__references = refer
        self.__feeders = feed
        self.__interim = interim
        if store_as is None:
            self.__stored_reference_name = "generated_" + self.__name
        else:
            self.__stored_reference_name = "generated_" + store_as
        from swayam import Template
        self.__template = getattr(Template, self.__template_name)
        
        if self.__singular_name is None:
            self.__singular_name = name
        if self.__plural_name is None:
            self.__plural_name = self.__singular_name + "s"
        if self.__description is None:
            self.__description = getattr(Template, self.__template_name).description
                
    @property
    def name(self):
        return self.__name
    
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
    def has_dependencies(self):
        if not self.__feeders and not self.__references:
            return False
        else:
            return True
        
    @property
    def references(self):
        return self.__references
    
    @property
    def feeders(self):
        return self.__feeders