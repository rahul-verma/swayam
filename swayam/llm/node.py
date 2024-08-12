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

from abc import abstractmethod
from typing import Union
from .prompt.request import *

class AgentNode:
    
    def __init__(self, wrapped_object):
        self.__wrapped_object = wrapped_object
    
    @property
    def wrapped_object(self):
        return self.__wrapped_object
    @property
    def blank_slate(self) -> bool:
        return self.__blank_slate
    
    @abstractmethod
    def reset(self) -> None:
        pass
    
    @classmethod
    def append_node(cls, raw_object, nodes) -> None:
        PromptNode._load(raw_object, nodes)
    
class PromptNode(AgentNode):
    
    def __init__(self, prompt_object):
        super().__init__(prompt_object)
        
    @property
    def prompt_sequence(self):
        return self.wrapped_object

    @classmethod
    def _load(clas, raw_node, nodes) -> None:
        from .prompt.request import Prompt        
        loaded_prompt_sequence = Prompt.load_prompt_object(raw_node)._get_first_child()
        nodes.append(PromptNode(loaded_prompt_sequence))
    
    