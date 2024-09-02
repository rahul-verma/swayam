
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

from swayam.llm.story.story import UserStory
from swayam.llm.thought.thought import UserThought
from swayam.llm.expression.expression import UserExpression
from swayam.llm.prompt.prompt import UserPrompt


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
        
    def fetch_value(self, phase, key):
        # Get the class name of the object
        class_name = phase.__class__.__name__

        # Start looking from the class_name in the order defined
        start_index = self.__order.index(class_name)

        # Traverse the __order list starting from the given class_name
        for key in self.__order[start_index:]:
            if key in self.__storage and self.__storage[key]:
                return self.__storage[key]

        # If nothing is found, return None or some default value
        return None
    
    def set_value(self, phase, key, value):
        self.__storage[phase.__class__.__name__][key] = value
        
    def set_value_in_parent(self, phase, key, value):
        kls = phase.__class__.__name__
        if kls == UserStory.__class__.__name__:
            raise ValueError("There is no parent for a UserStory")
        else:
            parent_index = self.__order.index(class_name) + 1
            parent = self.__order[parent_index]
            self.__storage[parent][key] = value
    
    def items(self, phase):
        # Get the class name of the object
        class_name = phase.__class__.__name__
        # Start looking from the class_name in the order defined
        start_index = self.__order.index(class_name)
        
        merged_dict = {}
        # Iterate over the reversed order
        for key in reversed(self.__order[start_index:]):
            if key in self.__storage:
                merged_dict.update(self.__storage[key])
        return merged_dict