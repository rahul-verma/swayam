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

import os
import json

class Drafter:
    
    def __init__(self, *, artifact, thought):
        self.__artifact = artifact
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        self.__file_path = os.path.join(Tarkash.get_option_value(SwayamOption.FOLIO_DRAFT_DIR), thought,  artifact.name + ".json")
        directory = os.path.dirname(self.__file_path)
        os.makedirs(directory, exist_ok=True)
        with open(self.__file_path, "w") as file:
            file.write(json.dumps([], indent=4))
            
    def draft(self, content):
        existing_content = None
        with open(self.__file_path, "r") as file:
            existing_content = json.loads(file.read())
            
        updated_content = existing_content
        with open(self.__file_path, "w") as file:
            if isinstance(content, str):
                content = {"content": content}
                updated_content.append(content)
            elif isinstance(content, dict):
                updated_content.append(content)
            else:
                updated_content.extend(content)
            file.write(json.dumps(updated_content, indent=4))