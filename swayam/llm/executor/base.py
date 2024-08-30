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
from typing import List, Union

from tarkash import TarkashObject, log_info, log_debug
from swayam.llm.config.request import RequestConfig
from swayam.llm.config.model import ModelConfig
from swayam.llm.config.report import ReportConfig
from tarkash.type.descriptor import DString, DNumber, DBoolean
from swayam.llm.request.types import SystemRequest
from pydantic import BaseModel

class BaseLLMExecutor(TarkashObject):
    
    _name = DString()
    _temperature = DNumber()
    _model = DString()
    
    """
    Base Class for All LLM Agents
    """
    def __init__(self, *, listener, name:str = "Swayam Agent", provider:str = None, model:str = None, temperature=0, system_request:Union[str,SystemRequest]=None, **kwargs):
        self.__model_config = ModelConfig(provider=provider, model=model)
        self.__request_config = RequestConfig(temperature=temperature, **kwargs)
        self.__listener = listener
        super().__init__(**kwargs)
        
        self._temperature = temperature
        self._provider = self.model_config.provider
        self._model = self.model_config.model
        self.load()
        
        self.__default_agent_system_request = "You are a helpful assistant who deliberates and provides useful answers to my queries."
        if system_request is None:
            self.__system_request = SystemRequest(text=self.__default_agent_system_request)
        elif isinstance(system_request, str):
            self.__system_request = SystemRequest(text=system_request) 
        elif isinstance(system_request, SystemRequest):
            self.__system_request = system_request
        else:
            TypeError(f"Invalid type for system_request: {type(system_request)}. Can be either str or SystemRequest.")

    @property
    def model_config(self):
        return self.__model_config
    
    @property
    def request_config(self):
        return self.__request_config
    
    @property
    def listener(self):
        return self.__listener
    
    @property
    def system_request(self):
        return self.__system_request
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def load(self, *args, **kwargs):
        pass