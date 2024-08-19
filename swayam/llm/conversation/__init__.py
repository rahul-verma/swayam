
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
from swayam.llm.structure.structure import IOStructure
from .meta import ConversationMeta

class Conversation(metaclass=ConversationMeta):
    
    @classmethod
    def prompts(cls, *prompts:UserPrompt, purpose:str=None, system_prompt:Union[str,SystemPrompt]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMConversation:
        if len(prompts) == 0:
            raise ValueError("No prompts provided.")
        for prompt in prompts:
            if not isinstance(prompt, UserPrompt):
                raise ValueError(f"Invalid prompt type: {type(prompt)}. Should be a UserPrompt object.")
        if system_prompt:
            if type(system_prompt) == str:
                system_prompt = SystemPrompt(text=system_prompt)
            elif not isinstance(system_prompt, SystemPrompt):
                raise ValueError(f"Invalid system prompt type: {type(system_prompt)}. Should be a string or a SystemPrompt object")
            
        from swayam import Tool, Structure
        if output_structure is not None and type(output_structure) is str:
            output_structure = getattr(Structure, output_structure)
        if tools is not None:
            output_tools = []
            for tool in tools:
                if type(tool) is str:
                    output_tools.append(getattr(Tool, tool))
                else:
                    output_tools.append(tool)
            tools = output_tools

        return LLMConversation(*prompts, purpose=purpose, system_prompt=system_prompt, image=image, output_structure=output_structure, tools=tools)
    
    @classmethod
    def texts(cls, *prompts:UserPrompt, purpose:str=None, system_prompt:Union[str,SystemPrompt]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMConversation:
        for prompt in prompts:
            if type(prompt) is not str:
                raise ValueError(f"Invalid prompt type: {type(prompt)}. Should be a string")
        return cls.prompts(*[UserPrompt(text=prompt) for prompt in prompts], purpose=purpose, system_prompt=system_prompt,  image=image, output_structure=output_structure, tools=tools)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return ConversationFormatter(**fmt_kwargs)
    
    