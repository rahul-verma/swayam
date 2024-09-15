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
    
    def __init__(self, *, artifact, file_path) -> None:
        self.__artifact = artifact
        self.__file_path = file_path
        
    def __getattr__(self, name):
        return getattr(self.__artifact, name)
    
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
    
    def load(self):
        with open(self.__file_path, "r") as file:
            return json.loads(file.read())
        
    def singular_writeup(self, content):
        return f"Following is the input data for this task:__NL____NL__### JSON Schema__NL__**This schema is only for you to understand the structure of the {self.singular_name} Content**. If I've asked you to review contents, then do not include review comments for this schema.__NL____NL__```{json.dumps(self.template.definition)}```__NL____NL__### {self.singular_name} Content__NL__As per the above schema, analyse the following data. It {self.description}__NL__**DONOT DO A SCHEMA REVIEW OF FOLLOWING DATA. REVIEW ONLY WHAT IT CONTAINS**.__NL____NL__```{json.dumps(content)}```__NL____NL__"
    
    def plural_writeup(self, contents):
        return f"Following is the input data for this task:__NL____NL__### JSON Schema__NL__**This schema is only for you to understand the structure of the individual entries in {self.plural_name} Content**. If I've asked you to review contents, then do not include review comments for this schema.__NL____NL__```{json.dumps(self.template.definition)}```__NL____NL__### {self.plural_name} Contents__NL__As per the above schema, analyse the following data presented as a JSON List. It {self.description}.__NL__**DONOT DO A SCHEMA REVIEW OF FOLLOWING DATA. REVIEW ONLY WHAT IT CONTAINS**.__NL____NL__```{json.dumps(contents)}```__NL____NL__"
    
    

class ReferenceMetaData:
    
    def __init__(self, *, artifact) -> None:
        self.__artifact = artifact
        
    def __call__(self, *, thought):
        # Look in Folio Artifacts
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        folio_draft_dir = Tarkash.get_option_value(SwayamOption.FOLIO_ARTIFACT_DIR)
        reference_file_path = os.path.join(folio_draft_dir, self.__artifact.file_name)
        if not os.path.exists(reference_file_path):
            # Look in Thought's Drafts
            folio_draft_dir = Tarkash.get_option_value(SwayamOption.FOLIO_DRAFT_DIR)
            reference_file_path = os.path.join(folio_draft_dir, thought, self.__artifact.file_name)
            if not os.path.exists(reference_file_path):
                from .error import ReferenceContentNotFoundError
                raise ReferenceContentNotFoundError(self, name=self.__artifact.name)
        
        return Reference(artifact=self.__artifact, file_path=reference_file_path)
