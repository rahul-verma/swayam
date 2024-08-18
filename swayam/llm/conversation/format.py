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

from swayam.llm.prompt.file import PromptFile
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from swayam.llm.prompt.format import PromptFormatter
from .conversation import LLMConversation
from swayam.llm.structure.structure import ResponseStructure

class ConversationFormatter:
    
    def __init__(self, **fmt_kwargs):
        self.__fmt_kwargs = fmt_kwargs

    def files(self, *prompt_files:PromptFile, system_prompt:Union[str,SystemPrompt]=None, image:str=None, response_format:Union[str, ResponseStructure]=None, tools:list=None) -> LLMConversation:
        if len(prompt_files) == 0:
            raise ValueError("No prompts provided.")
        prompts = []
        for prompt_file in prompt_files:
            if not isinstance(prompt_file, PromptFile):
                raise ValueError(f"Invalid prompt type: {type(prompt_file)}. Should be a PromptFile object.")  
            
            formatter = PromptFormatter(role=prompt_file.role, **self.__fmt_kwargs)
            prompt = getattr(formatter, prompt_file.file_name)
            prompts.append(prompt)
        
        from swayam import Conversation
        return Conversation.prompts(*prompts, system_prompt=system_prompt, image=image, response_format=response_format, tools=tools)