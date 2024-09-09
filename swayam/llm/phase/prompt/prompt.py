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
from swayam.inject.structure.structure import IOStructure


class UserPrompt:
    
    def __init__(self, *, text:str, purpose:str=None, image:str=None, output_structure:str=None, tools:list=None, resources=None, before=None, after=None, standalone:bool=False) -> None:
        self.__role = "user"
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Prompt"
        else:
            self.__purpose = f"Prompt: {self.__purpose}"
        self.__content = text
        self.__output_structure = output_structure
        self.__resources = resources
        self.__before = before
        self.__after = after
        if not self.__before:
            self.__before = []
        if not self.__after:
            self.__after = []

        self.__standalone = standalone
        
        if self.__output_structure is not None:
            from swayam import Structure
            self.__output_structure = getattr(Structure, self.__output_structure)
        
        self.__tools = tools
        self.__tool_definitions = None
        self.__tool_dict = {}
        
        if self.__tools:
            self.load_tools_from_names(self.__tools)
        
        self.__message = {
            "role": self.__role,
            "content": self.__content
        }
        
        if image:
            self.image = image
        else:
            self.__image = None
            self.__image_path = None
            
        self.__store = None
            
        from swayam.llm.enact.fixture import Fixture
        self.__fixture = Fixture(phase=self, before=self.__before, after=self.__after)

    @property
    def fixture(self):
        return self.__fixture
            
    @property
    def store(self):
        return self.__store
    
    @store.setter
    def store(self, store):
        if not self.__store:
            self.__store = store.get_phase_wrapper(self)
            self.__store["purpose"] = self.__purpose
            
    def load_tools_from_names(self, tool_names):
        from swayam import Tool
        self.__tools = [getattr(Tool, tool) for tool in tool_names]
        self.__tool_definitions = [tool.definition for tool in self.__tools]
        self.__tool_dict = {tool.name: tool for tool in self.__tools}

    def dynamic_format(self):
        updated_content = self.__message["content"]
        if self.image:
            updated_content = updated_content[0]["text"]
        #sanitized_text = updated_content.replace("\\", "\\\\")
        import re
        for key, value in self.store.items():
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
            
    def suggest_output_structure(self, structure_name):
        from swayam import Structure
        if not self.output_structure and structure_name:
            self.__output_structure = getattr(Structure, structure_name)
            
    def suggest_tools(self, tool_names):
        from swayam import Tool
        if not self.tools and tool_names:
            self.load_tools_from_names(tool_names)
        
    @property
    def purpose(self):
        return self.__purpose
            
    @property
    def output_structure(self):
        return self.__output_structure
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
            tool_response = tool(phase=self, **kwargs)
            from .response import ToolResponse
            return ToolResponse(tool_id=tool_id, tool_name=tool_name, content=tool_response)
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
    def is_directive(self):
        return self.__role == "system"