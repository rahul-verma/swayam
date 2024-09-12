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
    
import json

from copy import deepcopy
from typing import Any

from abc import ABC, abstractmethod
from swayam.inject.template.template import DataTemplate


class UserPrompt:
    
    def __init__(self, *, text:str, purpose:str=None, image:str=None, out_template:str=None, actions:list=None, prologue=None, epilogue=None, standalone:bool=False) -> None:
        self.__role = "user"
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Prompt"
        else:
            self.__purpose = f"Prompt: {self.__purpose}"
        self.__content = text
        self.__out_template = out_template
        self.__prologue = prologue
        self.__epilogue = epilogue
        if not self.__prologue:
            self.__prologue = []
        if not self.__epilogue:
            self.__epilogue = []

        self.__standalone = standalone
        
        if self.__out_template is not None:
            from swayam import Template
            self.__out_template = getattr(Template, self.__out_template)
        
        self.__actions = actions
        self.__action_definitions = None
        self.__action_dict = {}
        
        if self.__actions:
            self.load_actions_from_names(self.__actions)
        
        self.__message = {
            "role": self.__role,
            "content": self.__content
        }
        
        if image:
            self.image = image
        else:
            self.__image = None
            self.__image_path = None
            
        self.__standalone = standalone
            
        self.__vault = None
            
        from swayam.llm.enact.frame import Frame
        self.__frame = Frame(phase=self, prologue=self.__prologue, epilogue=self.__epilogue)

    @property
    def frame(self):
        return self.__frame
            
    @property
    def vault(self):
        return self.__vault
    
    @vault.setter
    def vault(self, vault):
        if not self.__vault:
            self.__vault = vault.get_phase_wrapper(self)
            self.__vault["purpose"] = self.__purpose
            
    def load_actions_from_names(self, action_names):
        from swayam import Action
        self.__actions = [getattr(Action, action) for action in action_names]
        self.__action_definitions = [action.definition for action in self.__actions]
        self.__action_dict = {action.name: action for action in self.__actions}

    def dynamic_format(self):
        updated_content = self.__message["content"]
        if self.image:
            updated_content = updated_content[0]["text"]
        #sanitized_text = updated_content.replace("\\", "\\\\")
        import re
        for key, value in self.vault.items():
            if value is None:
                value = ""
            elif type(value) in (dict, list):
                value = json.dumps(value, indent=4)
            
            
            updated_content = updated_content.replace(f"${key}$", str(value))
            
        
        # Any leftovers, to assign an initial value of empty string
        updated_content = updated_content.replace(f"${key}$", "")
        
        if not self.image:
            self.__message = {
                "role": self.__role,
                "content": updated_content
            }
        else:
            self.__message["content"][0]["text"] = updated_content 
            
    def suggest_image(self, image):
        if not self.image:
            self.image = image
            
    def suggest_out_template(self, template_name):
        from swayam import Template
        if not self.out_template and template_name:
            self.__out_template = getattr(Template, template_name)
            
    def suggest_actions(self, action_names):
        from swayam import Action
        if not self.actions and action_names:
            self.load_actions_from_names(action_names)
        
    @property
    def purpose(self):
        return self.__purpose
            
    @property
    def out_template(self):
        return self.__out_template
    @property
    def actions(self):
        return tuple(self.__actions) if self.__actions else None
    
    @property
    def action_definitions(self):
        return self.__action_definitions
    
    @property
    def action_dict(self):
        return self.__action_dict
    
    def call_action(self, action_id, action_name, **kwargs):
        tool = self.__action_dict.get(action_name)
        if tool:
            action_response = tool(phase=self, **kwargs)
            from .response import ActionResponse
            return ActionResponse(action_id=action_id, action_name=action_name, content=action_response)
        else:
            raise ValueError(f"Action {action_name} not defined for this prompt.")

    def process_for_report(self):
        
        if not self.image:
            self.__reportable_message = deepcopy(self.__message)
            self.__reportable_text = self.__message["content"]
        else:
            self.__reportable_message = deepcopy(self.__message)
            temp_content = self.__reportable_message["content"]
            self.__reportable_text = temp_content
            if type(temp_content) == list:
                for item in temp_content:
                    if item["type"] == "text":
                        self.__reportable_text = item["text"]
                        del item["text"]
                    elif item["type"] == "image_url":
                        prefix = self.__image.as_data_url.split(",")[0]
                        item["description"] = f"{prefix}, <Base64 encoded content of {self.__image_path}>."
                        item["local_path"] = self.__image_path
                        del item["image_url"]
            
        
    @property
    def message(self):
        return self.__message
    
    @property
    def content(self):
        return self.__message["content"]
    
    @property
    def role(self):
        return self.__message["role"]
    
    @property
    def image_path(self):
        return self.__image_path
    
    @property
    def image(self):
        return self.__image
    
    @property
    def image_as_data_url(self):
        return self.__image.as_data_url if self.__image else None
    
    @image.setter
    def image(self, image):
        from tarkash import ImageFile
        image = ImageFile(image) if image else None
        self.__image_path = image.full_path
        self.__image = image
        self.__message["content"] = [
                                    {"type": "text", "text": self.__content},
                                    {"type": "image_url", "image_url": {"url": image.as_data_url}}
                                ]
    
    @property
    def reportable_text(self):
        return self.__reportable_text
    
    @property
    def reportable_content(self):
        return self.__reportable_message["content"]
    
    @property
    def reportable_message(self):
        return self.__reportable_message
    
    @property
    def is_standalone(self):
        return self.__standalone
    
    