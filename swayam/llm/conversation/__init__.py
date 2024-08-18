
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

from typing import Union

from tarkash import log_debug
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from swayam.llm.prompt.file import PromptFile
from .format import ConversationFormatter
from .conversation import LLMConversation
from swayam.llm.structure.structure import ResponseStructure

class Conversation:
    
    @classmethod
    def prompts(cls, *prompts:UserPrompt, system_prompt:Union[str,SystemPrompt]=None, image:str=None, response_format:Union[str, ResponseStructure]=None, tools:list=None) -> LLMConversation:
        if len(prompts) == 0:
            raise ValueError("No prompts provided.")
        for prompt in prompts:
            if not isinstance(prompt, UserPrompt):
                raise ValueError(f"Invalid prompt type: {type(prompt)}. Should be a UserPrompt object.")
        if system_prompt:
            if type(system_prompt) == str:
                system_prompt = SystemPrompt(system_prompt)
            elif not isinstance(system_prompt, SystemPrompt):
                raise ValueError(f"Invalid system prompt type: {type(system_prompt)}. Should be a string or a SystemPrompt object")
        return LLMConversation(*prompts, system_prompt=system_prompt, image=image, response_format=response_format, tools=tools)
    
    @classmethod
    def texts(cls, *prompts:UserPrompt, system_prompt:Union[str,SystemPrompt]=None, image:str=None, response_format:Union[str, ResponseStructure]=None, tools:list=None) -> LLMConversation:
        for prompt in prompts:
            if type(prompt) is not str:
                raise ValueError(f"Invalid prompt type: {type(prompt)}. Should be a string")
        return cls.prompts(*[UserPrompt(text=prompt) for prompt in prompts], system_prompt=system_prompt,  image=image, response_format=response_format, tools=tools)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return ConversationFormatter(**fmt_kwargs)
    
    