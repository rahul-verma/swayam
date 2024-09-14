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


class Reference:
    
    def __init__(self, *, name, singular_name=None, plural_name=None, description=None, template=None) -> None:
        self.__name = name
        self.__file_name = name + ".json"
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        folio_draft_dir = Tarkash.get_option_value(SwayamOption.FOLIO_DRAFT_DIR)
        self.__file_path = os.path.join(folio_draft_dir, self.file_name)
        self.__singular_name = singular_name
        self.__plural_name = plural_name
        self.__description = description
        self.__template_name = template
    
        from swayam import Template
        self.__template = getattr(Template, self.__template_name)
                
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
    
    def load(self):
        with open(self.__file_path, "r") as file:
            return json.loads(file.read())
        
    def singular_writeup(self, content):
        return f"Following is the input data for this task:__NL____NL__### JSON Schema__NL__**This schema is only for you to understand the structure of the {self.__singular_name} Content**.__NL____NL__```{json.dumps(self.__template.definition)}```__NL____NL__### {self.__singular_name} Content__NL__As per the above schema, analyse the following data. It {self.__description}__NL____NL__```{json.dumps(content)}```__NL____NL__"
    
    def plural_writeup(self, contents):
        return f"Following is the input data for this task:__NL____NL__### JSON Schema__NL__**This schema is only for you to understand the structure of the individual entries in {self.__plural_name} Content**.__NL____NL__```{json.dumps(self.__template.definition)}```__NL____NL__### {self.__plural_name} Contents__NL__As per the above schema, analyse the following data presented as a JSON List. It {self.__description}__NL____NL__```{json.dumps(contents)}```__NL____NL__"
        