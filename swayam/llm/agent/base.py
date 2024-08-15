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
from typing import List

from tarkash import TarkashObject, log_info, log_debug
from swayam.llm.config.prompt import PromptConfig
from swayam.llm.config.model import ModelConfig
from swayam.llm.config.report import ReportConfig
from tarkash.type.descriptor import DString, DNumber, DBoolean
from swayam.llm.prompt.types import SystemPrompt
from pydantic import BaseModel

class BaseLLMAgent(TarkashObject):
    
    _name = DString()
    _temperature = DNumber()
    _model = DString()
    _content_only = DBoolean()
    _display = DBoolean()
    _report_html = DBoolean()
    _show_in_browser = DBoolean()
    
    """
    Base Class for All LLM Agents
    """
    def __init__(self, name:str = "Swayam Agent", provider:str = None, model:str = None, temperature=0, system_prompt:SystemPrompt=None, display=False, report_html=True, show_in_browser=True, **kwargs):
        self.__model_config = ModelConfig(provider=provider, model=model)
        self.__prompt_config = PromptConfig(temperature=temperature, **kwargs)
        self.__report_config = ReportConfig(display=display, report_html=report_html, show_in_browser=show_in_browser)
        super().__init__(**kwargs)
        self._temperature = temperature
        self._provider = self.model_config.provider
        self._model = self.model_config.model
        self._display = display
        self._report_html = report_html
        self._show_in_browser = show_in_browser
        
    @property
    def model_config(self):
        return self.__model_config
    
    @property
    def prompt_config(self):
        return self.__prompt_config
    
    @property
    def report_config(self):
        return self.__report_config
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass