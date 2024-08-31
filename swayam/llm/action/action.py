
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

from typing import Any, Union

from tarkash import log_debug
from swayam.llm.request import Request
from swayam.llm.request.types import SystemRequest, UserRequest
from .context import ActionContext
from swayam.inject.structure.structure import IOStructure

class LLMAction:
    
    def __init__(self, *requests:Request, purpose:str=None, system_request:SystemRequest=None, context:ActionContext=None,  image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_context:bool=True, invoker_response_as:str=None) -> Any:
        self.__requests = list(requests)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Action"
        self.__agent_context = context
        self.__system_request = system_request
        self.__image = image
        self.__output_structure = output_structure
        self.__tools = tools
        self.__store_response_as = store_response_as
        self.__make_image_suggestions()
        self.__make_structure_suggestions()
        self.__make_tool_suggestions()
        
        # Depends on how it was created. When it is a single request action created for an execute call of Agent, it is treated as a continuation of the previous action.
        self.__extends_previous_action = False
        
        # If True, it gets an empty context value. Has no impact on context of the follow-up actions.
        self.__standalone = standalone
        
        # If True, it resets the parent's context for itself. The subsequent action receives the context that it results in.
        self.__reset_context = reset_context
        
    @property
    def should_store_response(self):
        return self.__store_response_as is not None
    
    @property
    def response_storage_name(self):
        return self.__store_response_as
        
    @property
    def standalone(self):
        return self.__standalone
    
    @property
    def reset_context(self):
        return self.__reset_context
        
    @property
    def extends_previous_action(self):
        return self.__extends_previous_action
    
    @extends_previous_action.setter
    def extends_previous_action(self, value:bool):
        self.__extends_previous_action = value
        
    @property
    def extends_previous_action(self):
        return self.__extends_previous_action
    
    @extends_previous_action.setter
    def extends_previous_action(self, value:bool):
        self.__extends_previous_action = value

    def __make_image_suggestions(self):
        # the image is appended only to the first request.
        if self.__image:
            self.__requests[0].suggest_image(self.__image)
        
    def __make_structure_suggestions(self):
        # Tools and response format are suggested to all requests.            
        for request in self.__requests:
            if self.__image:
                request.suggest_output_structure(self.__output_structure)
                
    def __make_tool_suggestions(self):
        # Tools and response format are suggested to all requests.            
        for request in self.__requests:
            if self.__tools:
                request.suggest_tools(self.__tools) 
    
    def is_new(self):
        return len(self.__agent_context.action_context) == 0
        
    def has_system_request(self):
        return self.__system_request is not None
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def system_request(self):
        return self.__system_request
        
    @system_request.setter
    def system_request(self, system_request:SystemRequest):
        self.__system_request = system_request
        
    @property
    def context(self):
        return self.__agent_context
    
    @context.setter
    def context(self, context:ActionContext):
        self.__agent_context = context
        
    def append(self, request:Request):
        self.__requests.append(request)
        
    def __len__(self):
        return len(self.__requests)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Action.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Action (Length: {len(self)})\n"
        
        for request in self.__requests:
            if isinstance(request, LLMAction):
                description += request.describe(level + 1)
            else:
                description += f"{indent}  {type(request).__name__}\n"
        
        return description
    
    @property
    def _requests(self):
        return self.__requests
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__requests[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
        
    def _get_first_child(self):
        return self.__requests[0]
    

    def suggest_image(self, image):
        if not self.__image:
            self.__image = image
        self.__make_image_suggestions()
            
    def suggest_output_structure(self, output_structure):
        if not self.__output_structure:
            self.__output_structure = output_structure
        self.__make_structure_suggestions()
            
    def suggest_tools(self, tools):
        if not self.__tools:
            self.__tools = tools
        self.__make_tool_suggestions()
            