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

class PromptFormatter:
    
    def __init__(self, *, role, **kwargs):
        self.__role = role
        self.__kwargs = kwargs
        
    def __getattr__(self, name):
        from .namespace import PromptDir
        import yaml
        with open(PromptDir.get_path_for_prompt(role=self.__role, name=name)) as f:
            content = yaml.safe_load(f.read().format(**self.__kwargs))
        return PromptDir.create_prompt_from_content(content)

class FormatterMediator:
    def __init__(self, *, role):
        self.__role = role
        
    def __call__(self, **kwargs):
        return PromptFormatter(role=self.__role, **kwargs)