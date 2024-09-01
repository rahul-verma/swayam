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
from swayam.llm.config.prompt import PromptConfig
from swayam.llm.config.model import ModelConfig
from swayam.llm.config.report import RecorderConfig
from tarkash.type.descriptor import DString, DNumber, DBoolean
from swayam.llm.prompt.types import Perspective
from pydantic import BaseModel

class BaseLLMEnactor(TarkashObject):
    
    _name = DString()
    _temperature = DNumber()
    _model = DString()
    
    """
    Base Class for All LLM Narrators
    """
    def __init__(self, *, listener, name:str = "Swayam Narrator", provider:str = None, model:str = None, temperature=0, perspective:Union[str,Perspective]=None, **kwargs):
        self.__model_config = ModelConfig(provider=provider, model=model)
        self.__prompt_config = PromptConfig(temperature=temperature, **kwargs)
        self.__listener = listener
        super().__init__(**kwargs)
        
        self._temperature = temperature
        self._provider = self.model_config.provider
        self._model = self.model_config.model
        self.load()
        
        self.__default_narrator_perspective = "You are a helpful assistant who deliberates and provides useful answers to my queries."
        if perspective is None:
            self.__perspective = Perspective(text=self.__default_narrator_perspective)
        elif isinstance(perspective, str):
            self.__perspective = Perspective(text=perspective) 
        elif isinstance(perspective, Perspective):
            self.__perspective = perspective
        else:
            TypeError(f"Invalid type for perspective: {type(perspective)}. Can be either str or Perspective.")

    @property
    def model_config(self):
        return self.__model_config
    
    @property
    def prompt_config(self):
        return self.__prompt_config
    
    @property
    def listener(self):
        return self.__listener
    
    @property
    def perspective(self):
        return self.__perspective
    
    @abstractmethod
    def enact(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def load(self, *args, **kwargs):
        pass