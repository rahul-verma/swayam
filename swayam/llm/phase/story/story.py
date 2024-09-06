
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

from typing import Any, Union

from tarkash import log_debug

class UserStory:
    
    def __init__(self, *, thoughts, purpose:str=None, directive:str=None, resources=None, before=None, after=None) -> Any:
        self.__thought_names = list(thoughts)
        self.__thoughts = []
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Story"
        else:
            self.__purpose = f"Story: {self.__purpose}"
        self.__directive = directive
        self.__resources = resources
        self.__before = before
        self.__after = after
        
        self.__narrative = None
        
    def load(self, *, thought_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Structure
        from swayam.llm.phase.thought.namespace import ThoughtNamespace
        for thought_name in self.__thought_names:
            thought_namespace = ThoughtNamespace(path=thought_ns_path, resolution=resolution).formatter(**fmt_kwargs) 
            self.__thoughts.append(getattr(thought_namespace, thought_name))
        
    def has_directive(self):
        return self.__directive is not None
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def directive(self):
        return self.__directive
        
    @directive.setter
    def directive(self, directive):
        self.__directive = directive
        
    @property
    def narrative(self):
        return self.__narrative
    
    @narrative.setter
    def narrative(self, narrative):
        self.__narrative = narrative
        
    def __len__(self):
        return len(self.__thoughts)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Expression.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Thought (Length: {len(self)})\n"
        
        for thought in self.__thoughts:
            description += thought.describe(level + 1)
        
        return description
    
    @property
    def _thoughts(self):
        return self.__thoughts
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__thoughts[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
            