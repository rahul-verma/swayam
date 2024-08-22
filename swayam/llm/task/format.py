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

from swayam.llm.conversation.file import ConversationFile
from swayam.llm.conversation.conversation import LLMConversation
from swayam.llm.prompt.file import PromptFile
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from swayam.llm.prompt.format import PromptFormatter
from swayam.structure.structure import IOStructure

class TaskFormatter:
    
    def __init__(self, **fmt_kwargs):
        self.__fmt_kwargs = fmt_kwargs

    def conversation_files(self, *conversation_files:ConversationFile, purpose:str=None, system_prompt:PromptFile=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMConversation:
        from swayam.llm.conversation.format import ConversationFormatter
        from swayam.llm.task.repeater import DynamicConversationFile
        
        if len(conversation_files) == 0:
            raise ValueError("No conversations provided.")
        conversations = []
        for conversation_file in conversation_files:
            if isinstance (conversation_file, DynamicConversationFile):
                out_conversations = conversation_file.create_conversations(**self.__fmt_kwargs)
                conversations.extend(out_conversations)
            elif isinstance(conversation_file, ConversationFile):
                formatter = ConversationFormatter(**self.__fmt_kwargs)
                conversation = getattr(formatter, conversation_file.file_name)
                conversations.append(conversation)
            else:
                raise ValueError(f"Invalid conversation type: {type(conversation_file)}. Should be a ConversationFile object.") 
            
        if system_prompt:
            if not isinstance(system_prompt, PromptFile) and not isinstance(system_prompt, SystemPrompt):
                raise ValueError(f"Invalid system prompt type: {type(system_prompt)}. Should be a SystemPrompt or PromptFile object.")  
            elif not system_prompt.role == "system":
                raise ValueError(f"Invalid prompt role: {system_prompt.role}. Should be a system prompt.")
            
            if isinstance(system_prompt, PromptFile):
                system_formatter = PromptFormatter(role=system_prompt.role, **self.__fmt_kwargs)
                system_prompt = getattr(system_formatter, system_prompt.file_name)
                if not isinstance(system_prompt, SystemPrompt):
                    raise ValueError(f"There has been a critical framework issue in creating a system prompt.")
            else:
                # If a system prompt is provided directly, it is NOT formatted.
                pass
        
        from swayam import Task
        return Task.conversations(*conversations, purpose=purpose, system_prompt=system_prompt, image=image, output_structure=output_structure, tools=tools)
    
    def __getattr__(self, name):
        from .namespace import TaskDir
        import yaml
        with open(TaskDir.get_path_for_task(name=name)) as f:
            content = yaml.safe_load(f.read().format(**self.__fmt_kwargs))
        return TaskDir.create_task_from_content(name, content, **self.__fmt_kwargs)