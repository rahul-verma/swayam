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

import os

class TaskDir:
    
    def __init__(self, *, role):
        self._role = role
        
    @classmethod
    def get_path_for_task(cls, *, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        return os.path.join(Tarkash.get_option_value(SwayamOption.TASK_DIR), f"{name}.yaml")
    @classmethod
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_task_from_content(cls, name, content, **fmt_kwargs):
        from swayam import Task, Conversation, Prompt
        from swayam.llm.prompt.namespace import PromptDir
        from swayam.llm.prompt.format import PromptFormatter
        from swayam.llm.conversation.namespace import ConversationDir
        from swayam.llm.conversation.format import ConversationFormatter
        
        def load_system_prompt_from_direct_content(prompt):
            return PromptDir.create_prompt_from_content("system", f"{name}_system_prompt", prompt)
        
        def load_system_prompt_from_definition(definition):                
            if fmt_kwargs:
                prompt_file = getattr(getattr(Prompt.file, "system"), definition.strip())
                system_formatter = PromptFormatter(role="system", **fmt_kwargs)
                return getattr(system_formatter, prompt_file.file_name)
            else:
                return getattr(getattr(Prompt, "system"), definition.strip())
        
        def load_conversations_from_direct_content(conversations):
            conversation_objects = []
            for index, conversation in enumerate(conversations):
                if type(conversation) in (str, dict):
                    conversation_objects.append(ConversationDir.create_conversation_from_content(f"{name}_conversation{index+1}", conversation))
                else:
                    raise ValueError(f"Invalid format of conversation in task file: {name}. Expected a string or a dictionary. Found: {type(conversation)}")
            
            return Task.conversations(*conversation_objects, **task_kwargs)
        
        def load_conversations_from_definitions(role, definitions):
            
            for index, definition in enumerate(definitions):
                if type(definition) is not str:
                    raise ValueError(f"Invalid format of conversation definition in task file: {name}. Expected a string. Found: {type(definition)}")
                
            if fmt_kwargs:
                conversation_files = []
                for index, definition in enumerate(definitions):
                    conversation_files.append(getattr(getattr(Conversation.file, role), definition.strip()))
                return Task.formatter(**fmt_kwargs).conversation_files(*conversation_files, **task_kwargs)
            else:
                conversation_objects = []
                for index, definition in enumerate(definitions):
                    conversation_objects.append(getattr(getattr(Prompt, role), definition.strip()))
                return Task.prompts(*conversation_objects, **task_kwargs) 
            
        task_kwargs ={
            "purpose": content.get("purpose", cls._create_purpose_from_file_name(name)),
            "system_prompt": content.get("system_prompt", None),
            "image": content.get("image", None),
            "output_structure": content.get("output_structure", None),
            "tools": content.get("tools", None)
        }
        
        if type(content) is not dict:
            raise TypeError(f"Invalid format of task file: {name}. Expected a YAML dictionary with the allowed keys: [system_prompt, system_prompt_def, conversations, conversation_defs, purpose, image, output_structure, tools]")  
        
        if "conversations" in content and "conversation_defs" in content:
            raise ValueError(f"A task file cannot contain both 'conversations' and 'conversation_defs' keys. Choose one.")
        
        if "system_prompt" in content and "system_prompt_def" in content:
            raise ValueError(f"A task file cannot contain both 'system_prompt' and 'system_prompt_def' keys. Choose one.")
        
        if "system_prompt" in content:
            if type(content["system_prompt"]) is not str:
                raise ValueError(f"The system_prompt key in a conversation file must be a string. Found: {type(content['system_prompt'])}") 
            task_kwargs["system_prompt"] = load_system_prompt_from_direct_content(content["system_prompt"])
        elif "system_prompt_def" in content:
            if type(content["system_prompt_def"]) is not str:
                raise ValueError(f"The system_prompt_def key in a conversation file must be a string. Found: {type(content['system_prompt_def'])}") 
            task_kwargs["system_prompt"]  = load_system_prompt_from_definition(content["system_prompt_def"])

        for key, allowed_type in [("purpose", str), ("image", str), ("output_structure",str), ("tools", list)]:
            if key in content:
                if type(content[key]) is not allowed_type:
                    raise ValueError(f"Invalid format of '{key}' key in conversation file: {name}. Expected a {allowed_type}. Found: {type(content[key])}")
        
        if "conversations" in content:
            if type(content["conversations"]) is not list:
                raise ValueError(f"The conversations key in a task file must contain a list. Found: {type(content['conversations'])}") 
            return load_conversations_from_direct_content(content["conversations"])
        elif "conversation_defs" in content:
            if type(content["conversation_defs"]) is not list:
                raise ValueError(f"The conversation_defs key in a task file must contain a list. Found: {type(content['conversation_defs'])}") 
            return load_conversations_from_definitions(content["conversation_defs"])
        else:
            raise ValueError(f"A task file must contain either a 'conversations' or 'conversation_defs' key.") 

    @classmethod    
    def load_task_from_file(cls, name):
        from tarkash import YamlFile        
        file = YamlFile(cls.get_path_for_task(name=name))
        return cls.create_task_from_content(name, file.content)