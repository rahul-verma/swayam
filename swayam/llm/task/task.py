
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
from swayam.llm.conversation.conversation import LLMConversation
from swayam.llm.prompt.types import SystemPrompt
from swayam.llm.conversation.context import ConversationContext
from swayam.inject.structure.structure import IOStructure

class LLMTask:
    
    def __init__(self, *conversations:LLMConversation, purpose:str=None, system_prompt:SystemPrompt=None, content:ConversationContext=None,  image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> Any:
        self.__conversations = list(conversations)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Task"
        self.__context = None
        self.__system_prompt = system_prompt
           
        for conversation in self.__conversations:
            if image:
                conversation.suggest_image(image)
                
            if output_structure:
                conversation.suggest_output_structure(output_structure)
                
            if tools:
                conversation.suggest_tools(tools)
    
    def is_new(self):
        return len(self.__context) == 0
        
    def has_system_prompt(self):
        return self.__system_prompt is not None
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def system_prompt(self):
        return self.__system_prompt
        
    @system_prompt.setter
    def system_prompt(self, system_prompt:SystemPrompt):
        self.__system_prompt = system_prompt
        
    @property
    def context(self):
        return self.__context
    
    @context.setter
    def context(self, context:ConversationContext):
        self.__context = context
        
    def append(self, conversation:LLMConversation):
        self.__prompts.append(conversation)
        
    def __len__(self):
        return len(self.__conversations)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Conversation.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Conversation (Length: {len(self)})\n"
        
        for conversation in self.__conversations:
            description += conversation.describe(level + 1)
        
        return description
    
    @property
    def _conversations(self):
        return self.__prompts
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__conversations[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
        
    def _get_first_child(self):
        return self.__conversations[0]