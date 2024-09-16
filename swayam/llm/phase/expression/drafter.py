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
    
    def __init__(self, *, artifact, thought, draft_name=None, mode="overwrite"):
        self.__artifact = artifact
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        if draft_name is None:
            draft_name = artifact.name
        self.__file_path = os.path.join(Tarkash.get_option_value(SwayamOption.FOLIO_DRAFT_DIR), thought,  draft_name + ".json")
        directory = os.path.dirname(self.__file_path)
        
        if mode == "overwrite":
            os.makedirs(directory, exist_ok=True)
            with open(self.__file_path, "w") as file:
                begin_content = {
                    "artifact": artifact.name,
                    "contents": []
                }
                file.write(json.dumps(begin_content, indent=4))
        
        reference_name = "generated_" + self.__artifact.reference_name
            
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        ref_dir = Tarkash.get_option_value(SwayamOption.FOLIO_ARTIFACT_DIR)
        os.makedirs(ref_dir, exist_ok=True)
        self.__artifact_path = os.path.join(ref_dir, reference_name + ".json")
        
            
    def draft(self, content):
        existing_content = None
        with open(self.__file_path, "r") as file:
            existing_content = json.loads(file.read())
            
        updated_content = existing_content["contents"]
        with open(self.__file_path, "w") as file:
            if isinstance(content, str):
                updated_content.append(content)
            elif isinstance(content, dict):
                updated_content.append(content)
            else:
                updated_content.extend(content)
            existing_content["contents"] = updated_content
            file.write(json.dumps(existing_content, indent=4))
            
        self.export()
            
    def export(self):
        if self.__artifact.interim:
            return
        shutil.copy(self.__file_path, self.__artifact_path)
        