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

class StructureFileLoader:
    
    def __init__(self):
        pass
    
    def __getattr__(self, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        self.__base_path = Tarkash.get_option_value(SwayamOption.PROMPT_ROOT_DIR)
        file = YamlFile(os.path.join(self.__base_path, f"{name}.yaml"))
        
        text = None
        image = None
        
        content = file.content
        if type(content) is not dict:
            raise ValueError(f"Structure file {name} should be dictionary of fields")
        
        for name, field_content in content.items():
            if type(field_content) is not dict or "type" not in field_content or "desc" not in field_content:
                raise ValueError(f"Structure file {name} contains an invalid field definition {field_content} for {name}. Expected a dictionary with keys: [type, desc]")
            
            
                
            if field == "prompt":
                text = field_content
            elif field == "image":
                image = field_content

        from swayam import Prompt
        return Prompt.user_prompt(text, image=image)