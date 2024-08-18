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

from abc import ABC, abstractmethod
from swayam.llm.structure.structure import ResponseStructure


class BasePrompt(ABC):
    
    def __init__(self, *, role, text, purpose=None, image=None, response_format:ResponseStructure=None, tools=None) -> Any:
        self.__role = role
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"{role.title()} Prompt"
        self.__content = text
        self.__response_format = response_format
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
            
        self.__tool_definitions = None
        self.__tool_dict = {}
        if tools is not None:
            self.__tool_definitions = [tool.definition for tool in tools]
            self.__tool_dict = {tool.name: tool for tool in tools}
            
    def suggest_image(self, image):
        if not self.image:
            self.image = image
            
    def suggest_response_format(self, response_format):
        if not self.response_format:
            self.__response_format = response_format
            
    def suggest_tools(self, tools):
        if not self.tools:
            self.__tools = tools
            self.__tool_definitions = [tool.definition for tool in tools]
            self.__tool_dict = {tool.name: tool for tool in tools}
        
    @property
    def purpose(self):
        return self.__purpose
            
    @property
    def response_format(self):
        return self.__response_format
    @property
    def tools(self):
        return tuple(self.__tools) if self.__tools else None
    
    @property
    def tool_definitions(self):
        return self.__tool_definitions
    
    @property
    def tool_dict(self):
        return self.__tool_dict
    
    def call_tool(self, tool_id, tool_name, **kwargs):
        tool = self.__tool_dict.get(tool_name)
        if tool:
            tool_response = tool(**kwargs)
            tool_response.tool_id = tool_id
            return tool_response
        else:
            raise ValueError(f"Tool {tool_name} not defined for this prompt.")

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
    def is_system_prompt(self):
        return self.__role == "system"
