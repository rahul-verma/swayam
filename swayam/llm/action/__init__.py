
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
from swayam.llm.request.types import SystemRequest, UserRequest
from swayam.llm.request.file import RequestFile
from .format import ActionFormatter
from .action import LLMAction
from swayam.inject.structure.structure import IOStructure
from .meta import ActionMeta

class Action(metaclass=ActionMeta):
    
    @classmethod
    def requests(cls, *requests:UserRequest, purpose:str=None, system_request:Union[str,SystemRequest]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_context:bool=True, invoker_response_as:str=None) -> LLMAction:
        if len(requests) == 0:
            raise ValueError("No requests provided.")
        for request in requests:
            if not isinstance(request, UserRequest):
                raise ValueError(f"Invalid request type: {type(request)}. Should be a UserRequest object.")
        if system_request:
            if type(system_request) == str:
                system_request = SystemRequest(text=system_request)
            elif not isinstance(system_request, SystemRequest):
                raise ValueError(f"Invalid system request type: {type(system_request)}. Should be a string or a SystemRequest object")
            
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

        return LLMAction(*requests, purpose=purpose, system_request=system_request, image=image, output_structure=output_structure, tools=tools, reset_context=reset_context, standalone=standalone, invoker_response_as=store_response_as)
    
    @classmethod
    def texts(cls, *requests:UserRequest, purpose:str=None, system_request:Union[str,SystemRequest]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_context:bool=True, invoker_response_as:str=None) -> LLMAction:
        for request in requests:
            if type(request) is not str:
                raise ValueError(f"Invalid request type: {type(request)}. Should be a string")
        return cls.requests(*[UserRequest(text=request) for request in requests], purpose=purpose, system_request=system_request,  image=image, output_structure=output_structure, tools=tools, reset_context=reset_context, standalone=standalone, invoker_response_as=store_response_as)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return ActionFormatter(**fmt_kwargs)