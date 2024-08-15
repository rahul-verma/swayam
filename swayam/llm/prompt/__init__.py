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

from copy import deepcopy
from typing import Any


class Prompt:
    
    def __init__(self, *, role, text, system_prompt=None, image=None, tools=None) -> Any:
        self.__role = role
        self.__content = text
        self.__tools = tools
        
        self.__message = {
            "role": self.__role,
            "content": self.__content
        }
        if image:
            self.image = image
        else:
            self.__image = None
            self.__image_path = None
            
        self.__system_prompt = system_prompt
        
    @property
    def tools(self):
        return tuple(self.__tools) if self.__tools else None
            
    def set_system_prompt(self, prompt):
        self.__system_prompt = prompt
    
    @property
    def system_prompt(self):
        return self.__system_prompt

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
    
    @classmethod
    def as_user(cls, *texts, image=None, tools=None):
        from .converse import Conversation
        nodes = [{"role": "user", "text": text} for text in texts]
        if len(nodes) == 1:
            nodes = nodes[0]
        return Conversation.load_message(nodes, image=image, tools=tools)
    
    @classmethod
    def as_system(cls, node, *, image=None, tools=None):
        from .converse import Conversation
        output = Conversation.load_message({"role": "system", "text": node}, image=image, tools=tools)
        if isinstance(output, Conversation):
            return output._get_first_child()
        else:
            return output
    
    @property
    def is_system_prompt(self):
        return self.__role == "system"
