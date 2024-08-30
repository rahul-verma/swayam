
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
from swayam.llm.action.action import LLMAction
from swayam.llm.action.repeater import DynamicActionFile
from .task import LLMTask
from swayam.inject.structure.structure import IOStructure

from .format import TaskFormatter
from .meta import TaskMeta

class Task(metaclass=TaskMeta):
    
    @classmethod
    def actions(cls, *actions:LLMAction, purpose:str=None, system_request:Union[str,SystemRequest]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMTask:
        if len(actions) == 0:
            raise ValueError("No actions provided.")
        out_actions = []
        for action in actions:
            if isinstance (action, DynamicActionFile):
                repeated_actions = action.create_actions()
                out_actions.extend(repeated_actions)
            elif isinstance(action, LLMAction):
                out_actions.append(action)
            else:
                raise ValueError(f"Invalid action type: {type(action)}. Should be an LLMAction or DynamicActionFile object.")
            
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
        return LLMTask(*out_actions, purpose=purpose, system_request=system_request, image=image, output_structure=output_structure, tools=tools)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return TaskFormatter(**fmt_kwargs)