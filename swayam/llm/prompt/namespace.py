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
from .prompt import UserPrompt
from swayam.namespace.namespace import Namespace
from swayam.namespace.error import *

class PromptNamespace(Namespace):
    
    def __init__(self, path, resolution=None):
        super().__init__(type="Prompt", path=path, resolution=resolution)  

    def handle_current_name_as_dir(self, *, name, path, resolution):
        raise DefinitionNameNotAFileError(self, name=name)
    
    def handle_current_name_as_definition(self, *, name, path, resolution, purpose, content):
        from swayam import Structure
        
        import yaml
        content = yaml.safe_load(content)
        if isinstance(content, str):
            return UserPrompt(text=content, purpose=purpose)
        elif isinstance(content, dict):
            try:
                return UserPrompt(**Structure.Prompt(**content).as_dict())
            except Exception as e:
                raise DefinitionIsInvalidError(self, name=name, path=path, resolution=resolution, error=f"Allowed dictionary keys are [{Structure.Prompt.keys}]. Error: {e}")
        else:
            raise DefinitionIsInvalidError(name, path=path, resolution=resolution, error=f"Expected string or dict, got {type(content)}")
        
        
