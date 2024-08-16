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

import os

from tarkash.core.tobj import TarkashObject
from tarkash.type.descriptor import *
from abc import abstractmethod
from typing import List

class Model(TarkashObject):
    _provider = DString()
    _model_name = DString()
    _temperature = DFloat()
    
    def __init__(self, *, provider:str, model:str, **kwargs):
        tobj_kwargs = dict()
        tobj_kwargs.update(kwargs)
        tobj_kwargs["provider"] = provider
        tobj_kwargs["model_name"] = model
        super().__init__(**tobj_kwargs)
        self._provider = provider
        self._model_name = model
        self._model_kwargs = kwargs
        self._client = None
        self._create_client()
        
    @property
    def client(self):
        return self._client
    
    @property
    def model_name(self):
        return self._model_name
        
    @abstractmethod
    def _create_client(self):
        pass
    
    @abstractmethod
    def execute_messages(self, message:str, **kwargs):
        pass
        
        
    @staticmethod
    def create_client(*, config, prompt_config):

        class OpenAIModelClient(Model):
            def __init__(self, model, *, temperature:float=0, **kwargs):
                super().__init__(provider="openai", model=model, temperature=temperature, **kwargs)
                
            def _create_client(self):
                from openai import OpenAI
                self._client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
                
            def execute_messages(self, *, messages, response_format=None, tools=None):
                from pprint import pprint
                if tools:
                    tools =[tool.definition for tool in tools]

                if response_format is None:
                    return self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        tools=tools,
                        **self._model_kwargs
                    )
                else:
                    return self.client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        response_format=response_format,
                        **self._model_kwargs
                    )

        model_classes = {
            "openai": OpenAIModelClient
        }
        
        return model_classes[config.provider](config.model, **prompt_config.model_kwargs)
        
    @staticmethod
    def gpt_4o_mini(**kwargs):    
        return Model.create_client("openai", "gpt-4o-mini", **kwargs)
        
    