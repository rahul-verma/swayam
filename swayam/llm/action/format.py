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

from swayam.llm.request.file import RequestFile
from swayam.llm.request.types import SystemRequest, UserRequest
from swayam.llm.request.format import RequestFormatter
from .action import LLMAction
from swayam.inject.structure.structure import IOStructure

class ActionFormatter:
    
    def __init__(self, **fmt_kwargs):
        self.__fmt_kwargs = fmt_kwargs

    def request_files(self, *request_files:RequestFile, purpose:str=None, system_request:RequestFile=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_context:bool=True, invoker_response_as:str=None) -> LLMAction:
        if len(request_files) == 0:
            raise ValueError("No requests provided.")
        requests = []
        for request_file in request_files:
            if not isinstance(request_file, RequestFile):
                raise ValueError(f"Invalid request type: {type(request_file)}. Should be a RequestFile object.")  
            
            formatter = RequestFormatter(role=request_file.role, **self.__fmt_kwargs)
            request = getattr(formatter, request_file.file_name)
            requests.append(request)
            
        if system_request:
            if not isinstance(system_request, RequestFile) and not isinstance(system_request, SystemRequest):
                raise ValueError(f"Invalid system request type: {type(system_request)}. Should be a SystemRequest or RequestFile object.")  
            elif not system_request.role == "system":
                raise ValueError(f"Invalid request role: {system_request.role}. Should be a system request.")
            
            if isinstance(system_request, RequestFile):
                system_formatter = RequestFormatter(role=system_request.role, **self.__fmt_kwargs)
                system_request = getattr(system_formatter, system_request.file_name)
                if not isinstance(system_request, SystemRequest):
                    raise ValueError(f"There has been a critical framework issue in creating a system request.")
            else:
                # If a system request is provided directly, it is NOT formatted.
                pass
        
        from swayam import Action
        return Action.requests(*requests, purpose=purpose, system_request=system_request, image=image, output_structure=output_structure, tools=tools, reset_context=reset_context, standalone=standalone, invoker_response_as=store_response_as)
    
    def __getattr__(self, name):
        from .namespace import ActionDir
        import yaml
        with open(ActionDir.get_path_for_action(name=name)) as f:
            content = yaml.safe_load(f.read().format(**self.__fmt_kwargs))
        return ActionDir.create_action_from_content(name, content, **self.__fmt_kwargs)