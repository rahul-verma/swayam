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

from abc import ABC, abstractmethod
from typing import List

class LLMClient(ABC):
    
    def __init__(self, *, provider:str, model:str, **kwargs):
        self._provider = provider
        self._model_name = model
        self._model_kwargs = kwargs
        self._client = None
        self._create_client()
    
    @property
    def model_name(self):
        return self._model_name
    
    @abstractmethod
    def _create_client(self):
        pass
    
    @abstractmethod
    def execute_messages(self, *, messages, output_structure=None, tools=None):
        pass

        
    