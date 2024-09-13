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


class Draft:
    
    def __init__(self, *, name, description, template, depends_on=None) -> None:
        self.__name = name
        self.__file_name = name + ".json"
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        folio_draft_dir = Tarkash.get_option_value(SwayamOption.FOLIO_DRAFT_DIR)
        self.__file_path = os.path.join(folio_draft_dir, self.file_name)
        self.__description = description
        self.__template_name = template
        if self.__template_name is None:
            self.__template_name = "TextContent"
        self.__depends_on = depends_on
        self.__dependencies = []
    
        from swayam import Template
        self.__template = getattr(Template, self.__template_name)
        
        from swayam.inject.draft import Draft as DraftFacade
        
        if self.__depends_on:
            for dependency in self.__depends_on:
                self.__dependencies.append(getattr(DraftFacade, dependency))
                
    @property
    def name(self):
        return self.__name
                
    @property
    def file_name(self):
        return self.__file_name
    
    @property
    def file_path(self):
        return self.__file_path
                
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
    def depends_on(self):
        return self.__depends_on
    
    @property
    def dependencies(self):
        return self.__dependencies
    
    def load(self):
        with open(self.__file_path, "r") as file:
            return json.loads(file.read())
        