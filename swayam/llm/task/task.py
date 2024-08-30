
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
from swayam.llm.action.action import LLMAction
from swayam.llm.request.types import SystemRequest
from swayam.llm.action.context import ActionContext
from swayam.inject.structure.structure import IOStructure

class LLMTask:
    
    def __init__(self, *actions:LLMAction, purpose:str=None, system_request:SystemRequest=None, content:ActionContext=None,  image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> Any:
        self.__actions = list(actions)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Task"
        self.__context = None
        self.__system_request = system_request
           
        for action in self.__actions:
            if image:
                action.suggest_image(image)
                
            if output_structure:
                action.suggest_output_structure(output_structure)
                
            if tools:
                action.suggest_tools(tools)
    
    def is_new(self):
        return len(self.__context) == 0
        
    def has_system_request(self):
        return self.__system_request is not None
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def system_request(self):
        return self.__system_request
        
    @system_request.setter
    def system_request(self, system_request:SystemRequest):
        self.__system_request = system_request
        
    @property
    def context(self):
        return self.__context
    
    @context.setter
    def context(self, context:ActionContext):
        self.__context = context
        
    def append(self, action:LLMAction):
        self.__requests.append(action)
        
    def __len__(self):
        return len(self.__actions)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Action.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Action (Length: {len(self)})\n"
        
        for action in self.__actions:
            description += action.describe(level + 1)
        
        return description
    
    @property
    def _actions(self):
        return self.__requests
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__actions[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
        
    def _get_first_child(self):
        return self.__actions[0]