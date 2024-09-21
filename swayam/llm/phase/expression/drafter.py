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

from swayam import Action, Template
from swayam.inject.template.builtin import *

import os
import re

import os
import json
import shutil

class Drafter:
    
    def __init__(self, *, entity, thought, aggregate_name, interim=False, blueprint_name=None, mode="overwrite", refer=None, feed=None, reset_conversation=True):
        self.__entity = entity
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        self.__aggregate_name = aggregate_name
            
        self.__references = refer
        self.__feeders = feed
        self.__interim = interim
        if blueprint_name is None:
            self.__blueprint_name = aggregate_name
        else:
            self.__blueprint_name = blueprint_name
        
        self.__file_path = os.path.join(Tarkash.get_option_value(SwayamOption.FOLIO_AGGREGATE_DIR), thought,  self.__aggregate_name + ".json")
        directory = os.path.dirname(self.__file_path)
        
        if mode == "overwrite":
            os.makedirs(directory, exist_ok=True)
            with open(self.__file_path, "w") as file:
                begin_content = {
                    "entity": entity.name,
                    "fragments": dict()
                }
                file.write(json.dumps(begin_content, indent=4))
            
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        ref_dir = Tarkash.get_option_value(SwayamOption.FOLIO_BLUEPRINT_DIR)
        os.makedirs(ref_dir, exist_ok=True)
        self.__blueprint_path = os.path.join(ref_dir, self.__blueprint_name + ".json")
        
    @property
    def entity(self):
        return self.__entity
            
    def draft(self, content):
        print(f"Drafting content: {content}")
        existing_content = None
        with open(self.__file_path, "r") as file:
            existing_content = json.loads(file.read())
            
        updated_content = existing_content["fragments"]
        with open(self.__file_path, "w") as file:
            if isinstance(content, dict):
                if content[self.__entity.primary_key] not in updated_content:
                    updated_content[content[self.__entity.primary_key]] = [content[self.__entity.content_key]]
                else:
                    updated_content[content[self.__entity.primary_key]].append(content[self.__entity.content_key])
            else:
                raise ValueError(f"Draft content generated by a prompt must be a dictionary. Found : >>{type(content)}<<. Data: {content}")
            existing_content["fragments"] = updated_content
            file.write(json.dumps(existing_content, indent=4))
            
        self.export()
            
    def export(self):
        if self.__interim:
            return
        shutil.copy(self.__file_path, self.__blueprint_path)
        
    @property
    def interim(self):
        return self.__interim
    
    @property
    def blueprint_name(self):
        return self.__blueprint_name
    
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
        