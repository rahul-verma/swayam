
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

from swayam.llm.phase.story.story import UserStory
from swayam.llm.phase.thought.thought import UserThought
from swayam.llm.phase.expression.expression import UserExpression
from swayam.llm.phase.prompt.prompt import UserPrompt
from functools import partial

class PhaseStore:
    
    def __init__(self, phase, store):
        self.__phase = phase
        self.__store = store
        
    def __getattr__(self, name):
        return self[name]
    
    def __getitem__(self, key):
        return self.__store.get(key, phase=self.__phase)
    
    def __setitem__(self, key, value):
        self.__store.set(key, value, phase=self.__phase)
        
    def items(self):
        return self.__store.items(phase=self.__phase)
    
    @property
    def phase_name(self):
        return self.__phase.__class__.__name__

class STEPStore:
    
    def __init__(self):
        self.__order = [
            UserPrompt.__name__,
            UserExpression.__name__,
            UserThought.__name__,
            UserStory.__name__
        ]
        self.__storage = {}
        for item in self.__order:
            self.__storage[item] = {}
        
    def reset(self):
        for item in self.__order:
            self.__storage[item] = {}
        
    def get(self, key, *, phase):
        # Get the class name of the object
        class_name = phase.__class__.__name__

        # Start looking from the class_name in the order defined
        start_index = self.__order.index(class_name)

        class_lookup_order = self.__order[start_index:]
        # Traverse the __order list starting from the given class_name
        for class_name in class_lookup_order:
            if class_name in self.__storage and key in self.__storage[class_name]:
                return self.__storage[class_name][key]

        # If nothing is found, return None or some default value
        return "NOT_SET"
    
    def set(self, key, value, *, phase):
        self.__storage[phase.__class__.__name__][key] = value
        
    def set_in_parent(self, key, value, *, phase):
        kls = phase.__class__.__name__
        if kls == UserStory.__class__.__name__:
            raise ValueError("There is no parent for a UserStory")
        else:
            parent_index = self.__order.index(kls) + 1
            parent = self.__order[parent_index]
            self.__storage[parent][key] = value
    
    def items(self, *, phase=None):
        if phase is not None:
            # Get the class name of the object
            class_name = phase.__class__.__name__
            # Start looking from the class_name in the order defined
            start_index = self.__order.index(class_name)
        else:
            start_index = 0
        
        merged_dict = {}
        # Iterate over the reversed order
        for key in reversed(self.__order[start_index:]):
            if key in self.__storage:
                merged_dict.update(self.__storage[key])
        return merged_dict.items()
    
    def _raw_items(self):
        return self.__storage.items()
    
    def get_phase_wrapper(self, phase):
        return PhaseStore(phase, self)
    

        