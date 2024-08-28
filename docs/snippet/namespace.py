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
from .snippet import StructuredSnippet
from .error import *

class SnippetDir:
    
    def __init__(self, path):
        self.path = path        
    
    def __getattr__(self, name):
        name_path = os.path.join(self.path, name)
        # Check without the yaml extension
        if os.path.exists(name_path):
            if os.path.isdir(name_path):
                return SnippetDir(name_path)
            else:
                raise TypeError("Snippet file should have a yaml extension: " + name_path)
        elif os.path.exists(name_path + ".yaml"):
            return self.file(name)
        else:
            raise SnippetDefinitionNotFoundError(name, path=self.path)
        
    def file(self, name):
        from tarkash import YamlFile
        def_path = self.path + "/" + name + ".yaml"
        content = YamlFile(def_path).content
        purpose = name.replace("_", " ").title()
        if isinstance(content, str):
            return StructuredSnippet(purpose=purpose, text=content)
        elif isinstance(content, dict):
            try:
                return StructuredSnippet(**content)
            except TypeError as e:
                if "unexpected keyword argument" in str(e):
                    raise SnippetDefinitionFormatError(name, path=def_path, error=f"Allowed dictionary keys are [purpose, text]. Error: {e}")
        else:
            raise SnippetDefinitionFormatError(name, path=def_path, error=f"Expected string or dict, got {type(content)}")
        
        
