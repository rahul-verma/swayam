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
        return os.path.join(Tarkash.get_option_value(SwayamOption.CONVERSATION_ROOT_DIR), f"{name}.yaml")
    @classmethod
    def _create_purpose_from_file_name(cls, name):
        return name.replace("_", " ").lower().title()
    
    @classmethod
    def create_conversation_from_content(cls, name, content):
        from swayam import Prompt
        user_prompts = None
        
        if type(content) is not dict:
            raise TypeError(f"Invalid format of conversation file: {name}. Expected a YAML dictionary with the allowed keys: [system_prompt, user_prompts, purpose, image, output_structure, tools]")    
        
        if "user_prompts" not in content:
            raise ValueError(f"A conversation file must contain a 'user_prompts' key with a list of prompts.")    
        
        if type(content["user_prompts"]) is not list:
            raise ValueError(f"The user_prompts key in a conversation file must contain a list. Found: {type(content['user_prompts'])}")    
        
        from swayam.llm.prompt.namespace import PromptDir
            
        user_prompts = []
        for index, prompt in enumerate(content["user_prompts"]):
            if type(prompt) in (str, dict):
                user_prompts.append(PromptDir.create_prompt_from_content("user", f"{name}_prompt_{index+1}", prompt))
            elif not isinstance(prompt, dict):
                raise ValueError(f"Invalid format of user prompt in conversation file: {name}. Expected a string or a dictionary. Found: {type(prompt)}")      

        from swayam import Conversation
        
        fmt_kwargs ={
            "purpose": content.get("purpose", cls._create_purpose_from_file_name(name)),
            "system_prompt": content.get("system_prompt", None),
            "image": content.get("image", None),
            "output_structure": content.get("output_structure", None),
            "tools": content.get("tools", None)
        }
        """
        *prompts:UserPrompt, purpose:str=None, system_prompt:Union[str,SystemPrompt]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None)
        """
        for key, allowed_type in [("purpose", str), ("image", str), ("output_structure",str), ("tools", list)]:
            if key in content:
                if type(content[key]) is not allowed_type:
                    raise ValueError(f"Invalid format of '{key}' key in conversation file: {name}. Expected a {allowed_type}. Found: {type(content[key])}")
                
        return Conversation.prompts(*user_prompts, **fmt_kwargs)
    @classmethod    
    def load_conversation_from_file(cls, name):
        from tarkash import YamlFile        
        file = YamlFile(cls.get_path_for_conversation(name=name))
        return cls.create_conversation_from_content(name, file.content)