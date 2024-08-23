
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
from swayam.llm.conversation.conversation import LLMConversation
from swayam.llm.conversation.repeater import DynamicConversationFile
from .task import LLMTask
from swayam.structure.structure import IOStructure

from .format import TaskFormatter
from .meta import TaskMeta

class Task(metaclass=TaskMeta):
    
    @classmethod
    def conversations(cls, *conversations:LLMConversation, purpose:str=None, system_prompt:Union[str,SystemPrompt]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMTask:
        if len(conversations) == 0:
            raise ValueError("No conversations provided.")
        out_conversations = []
        for conversation in conversations:
            if isinstance (conversation, DynamicConversationFile):
                repeated_conversations = conversation.create_conversations()
                out_conversations.extend(repeated_conversations)
            elif isinstance(conversation, LLMConversation):
                out_conversations.append(conversation)
            else:
                raise ValueError(f"Invalid conversation type: {type(conversation)}. Should be an LLMConversation or DynamicConversationFile object.")
            
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
        return LLMTask(*out_conversations, purpose=purpose, system_prompt=system_prompt, image=image, output_structure=output_structure, tools=tools)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return TaskFormatter(**fmt_kwargs)