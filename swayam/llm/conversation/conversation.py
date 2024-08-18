
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
from swayam.llm.prompt import Prompt
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from .context import PromptContext
from swayam.llm.structure.structure import ResponseStructure

class LLMConversation:
    
    def __init__(self, *prompts:Prompt, purpose:str=None, system_prompt:SystemPrompt=None, content:PromptContext=None,  image:str=None, response_format:Union[str, ResponseStructure]=None, tools:list=None) -> Any:
        self.__prompts = list(prompts)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Conversation"
        self.__context = None
        self.__system_prompt = system_prompt
        
        # the image is appended only to the first prompt.
        if image:
            prompts[0].suggest_image(image)
        
        # Tools and response format are suggested to all prompts.            
        for prompt in prompts:
            if response_format:
                prompt.suggest_response_format(response_format)
                
            if tools:
                prompt.suggest_tools(tools)
    
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
    def context(self, context:PromptContext):
        self.__context = context
        
    def append(self, prompt:Prompt):
        self.__prompts.append(prompt)
        
    def __len__(self):
        return len(self.__prompts)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Conversation.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Conversation (Length: {len(self)})\n"
        
        for prompt in self.__prompts:
            if isinstance(prompt, LLMConversation):
                description += prompt.describe(level + 1)
            else:
                description += f"{indent}  {type(prompt).__name__}\n"
        
        return description
    
    @property
    def _prompts(self):
        return self.__prompts
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__prompts[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
        
    def _get_first_child(self):
        return self.__prompts[0]