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
    
    def __init__(self, *, draft_info):
        self.__draft_info = draft_info
        self.__file_path = draft_info.file_path
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