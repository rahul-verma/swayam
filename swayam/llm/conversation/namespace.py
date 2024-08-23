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

class ConversationDir:
    
    def __init__(self, *, role):
        self._role = role
        
    @classmethod
    def get_path_for_conversation(cls, *, name):
        from tarkash import Tarkash, YamlFile
        from swayam.core.constant import SwayamOption
        return os.path.join(Tarkash.get_option_value(SwayamOption.CONVERSATION_DIR), f"{name}.yaml")
    @classmethod
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_conversation_from_content(cls, name, content, **fmt_kwargs):
        from swayam import Conversation , Prompt
        from swayam.llm.prompt.namespace import PromptDir
        from swayam.llm.prompt.format import PromptFormatter
        
        def load_prompts_from_direct_content(role, prompts):
            

            prompt_objects = []
            for index, prompt in enumerate(prompts):
                counter = ""
                if role == "user":
                    counter = f"_{index+1}"
                if type(prompt) in (str, dict):
                    prompt_objects.append(PromptDir.create_prompt_from_content(role, f"{name}_{role}_prompt{counter}", prompt))
                else:
                    raise ValueError(f"Invalid format of user prompt in conversation file: {name}. Expected a string or a dictionary. Found: {type(prompt)}")
            if role == "user":
                return Conversation.prompts(*prompt_objects, **conversation_kwargs)
            else:
                return prompt_objects[0]
        
        def load_prompts_from_definitions(role, definitions):
            
            for index, definition in enumerate(definitions):
                if type(definition) is not str:
                    raise ValueError(f"Invalid format of prompt definition in conversation file: {name}. Expected a string. Found: {type(definition)}")
                
            if fmt_kwargs:
                prompt_files = []
                for index, definition in enumerate(definitions):
                    prompt_files.append(getattr(getattr(Prompt.file, role), definition.strip()))
                if role == "user":
                    return Conversation.formatter(**fmt_kwargs).prompt_files(*prompt_files, **conversation_kwargs)
                else:
                    system_formatter = PromptFormatter(role=role, **fmt_kwargs)
                    return getattr(system_formatter, prompt_files[0].file_name)
            else:
                prompt_objects = []
                for index, definition in enumerate(definitions):
                    prompt_objects.append(getattr(getattr(Prompt, role), definition.strip()))
                if role == "user":
                    return Conversation.prompts(*prompt_objects, **conversation_kwargs) 
                else:
                    return prompt_objects[0]
            
        conversation_kwargs ={
            "purpose": content.get("purpose", cls._create_purpose_from_file_name(name)),
            "system_prompt": content.get("system_prompt", None),
            "image": content.get("image", None),
            "output_structure": content.get("output_structure", None),
            "tools": content.get("tools", None),
            "reset_context": content.get("reset_context", True),
            "standalone": content.get("standalone", False),
            "store_response_as": content.get("store_response_as", None),
        }
        
        if type(content) is not dict:
            raise TypeError(f"Invalid format of conversation file: {name}. Expected a YAML dictionary with the allowed keys: [system_prompt, prompts, prompt_defs, purpose, image, output_structure, tools]")  
        
        if "prompts" in content and "prompt_defs" in content:
            raise ValueError(f"A conversation file cannot contain both 'prompts' and 'prompt_defs' keys. Choose one.")
        
        if "system_prompt" in content and "system_prompt_def" in content:
            raise ValueError(f"A conversation file cannot contain both 'system_prompt' and 'system_prompt_def' keys. Choose one.")
        
        # System Prompt
        if conversation_kwargs["system_prompt"] is not None and type(conversation_kwargs["system_prompt"]) is not str:
            raise ValueError(f"Invalid format of 'system_prompt' key in conversation file: {name}. Expected a string. Found: {type(conversation_kwargs['system_prompt'])}")
        
        if "system_prompt" in content:
            if type(content["system_prompt"]) is not str:
                raise ValueError(f"The system_prompt key in a conversation file must be a string. Found: {type(content['system_prompt'])}") 
            conversation_kwargs["system_prompt"] = load_prompts_from_direct_content("system", [content["system_prompt"]])
        elif "system_prompt_def" in content:
            if type(content["system_prompt_def"]) is not str:
                raise ValueError(f"The system_prompt_def key in a conversation file must be a string. Found: {type(content['system_prompt_def'])}") 
            conversation_kwargs["system_prompt"]  = load_prompts_from_definitions("system", [content["system_prompt_def"]])
                   
        """
        *prompts:UserPrompt, purpose:str=None, system_prompt:Union[str,SystemPrompt]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None)
        """
        for key, allowed_type in [("purpose", str), ("image", str), ("output_structure",str), ("tools", list)]:
            if key in content:
                if type(content[key]) is not allowed_type:
                    raise ValueError(f"Invalid format of '{key}' key in conversation file: {name}. Expected a {allowed_type}. Found: {type(content[key])}")
        
        if "prompts" in content:
            if type(content["prompts"]) is not list:
                raise ValueError(f"The prompts key in a conversation file must contain a list. Found: {type(content['prompts'])}") 
            return load_prompts_from_direct_content("user", content["prompts"])
        elif "prompt_defs" in content:
            if type(content["prompt_defs"]) is not list:
                raise ValueError(f"The prompt_defs key in a conversation file must contain a list. Found: {type(content['prompt_defs'])}") 
            return load_prompts_from_definitions("user", content["prompt_defs"])
        else:
            raise ValueError(f"A conversation file must contain either a 'prompts' or 'prompt_defs' key.") 

    @classmethod    
    def load_conversation_from_file(cls, name):
        from tarkash import YamlFile        
        file = YamlFile(cls.get_path_for_conversation(name=name))
        return cls.create_conversation_from_content(name, file.content)