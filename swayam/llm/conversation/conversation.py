
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
from swayam.llm.structure.structure import IOStructure

class LLMConversation:
    
    def __init__(self, *prompts:Prompt, purpose:str=None, system_prompt:SystemPrompt=None, context:PromptContext=None,  image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_context:bool=True) -> Any:
        self.__prompts = list(prompts)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Conversation"
        self.__context = context
        self.__system_prompt = system_prompt
        self.__image = image
        self.__output_structure = output_structure
        self.__tools = tools
        self.__make_image_suggestions()
        self.__make_structure_suggestions()
        self.__make_tool_suggestions()
        
        # Depends on how it was created. When it is a single prompt conversation created for an execute call of Agent, it is treated as a continuation of the previous conversation.
        self.__extends_previous_conversation = False
        
        # If True, it gets an empty context value. Has no impact on context of the follow-up conversations.
        self.__standalone = standalone
        
        # If True, it resets the parent's context for itself. The subsequent conversation receives the context that it results in.
        self.__reset_context = reset_context
        
    @property
    def standalone(self):
        return self.__standalone
    
    @property
    def reset_context(self):
        return self.__reset_context
        
    @property
    def extends_previous_conversation(self):
        return self.__extends_previous_conversation
    
    @extends_previous_conversation.setter
    def extends_previous_conversation(self, value:bool):
        self.__extends_previous_conversation = value
        
    @property
    def extends_previous_conversation(self):
        return self.__extends_previous_conversation
    
    @extends_previous_conversation.setter
    def extends_previous_conversation(self, value:bool):
        self.__extends_previous_conversation = value

    def __make_image_suggestions(self):
        # the image is appended only to the first prompt.
        if self.__image:
            self.__prompts[0].suggest_image(self.__image)
        
    def __make_structure_suggestions(self):
        # Tools and response format are suggested to all prompts.            
        for prompt in self.__prompts:
            if self.__image:
                prompt.suggest_output_structure(self.__output_structure)
                
    def __make_tool_suggestions(self):
        # Tools and response format are suggested to all prompts.            
        for prompt in self.__prompts:
            if self.__tools:
                prompt.suggest_tools(self.__tools) 
    
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
    

    def suggest_image(self, image):
        if not self.__image:
            self.__image = image
        self.__make_image_suggestions()
            
    def suggest_output_structure(self, output_structure):
        if not self.__output_structure:
            self.__output_structure = output_structure
        self.__make_structure_suggestions()
            
    def suggest_tools(self, tools):
        if not self.__tools:
            self.__tools = tools
        self.__make_tool_suggestions()
            