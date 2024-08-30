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

from swayam.llm.action.file import ActionFile
from swayam.llm.action.action import LLMAction
from swayam.llm.request.file import RequestFile
from swayam.llm.request.types import SystemRequest, UserRequest
from swayam.llm.request.format import RequestFormatter
from swayam.inject.structure.structure import IOStructure

class TaskFormatter:
    
    def __init__(self, **fmt_kwargs):
        self.__fmt_kwargs = fmt_kwargs

    def action_files(self, *action_files:ActionFile, purpose:str=None, system_request:RequestFile=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMAction:
        from swayam.llm.action.format import ActionFormatter
        from swayam.llm.action.repeater import DynamicActionFile
        
        if len(action_files) == 0:
            raise ValueError("No actions provided.")
        actions = []
        for action_file in action_files:
            if isinstance (action_file, DynamicActionFile):
                out_actions = action_file.create_actions(**self.__fmt_kwargs)
                actions.extend(out_actions)
            elif isinstance(action_file, ActionFile):
                formatter = ActionFormatter(**self.__fmt_kwargs)
                action = getattr(formatter, action_file.file_name)
                actions.append(action)
            else:
                raise ValueError(f"Invalid action type: {type(action_file)}. Should be a ActionFile object.") 
            
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

        from swayam import Task
        return Task.actions(*actions, purpose=purpose, system_request=system_request, image=image, output_structure=output_structure, tools=tools)
    
    def __getattr__(self, name):
        from .namespace import TaskDir
        import yaml
        with open(TaskDir.get_path_for_task(name=name), "r", encoding="utf-8") as f:
            content = yaml.safe_load(f.read().format(**self.__fmt_kwargs))
        return TaskDir.create_task_from_content(name, content, **self.__fmt_kwargs)