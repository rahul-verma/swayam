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

from abc import abstractmethod
from typing import List

class Model:
        
    @staticmethod
    def create_client(*, config, prompt_config):
        from .openai import OpenAIClient
        model_classes = {
            "openai": OpenAIClient
        }
        
        return model_classes[config.provider](config.model, **prompt_config.model_kwargs)
        
    @staticmethod
    def gpt_4o_mini(**kwargs):    
        return Model.create_client("openai", "gpt-4o-mini", **kwargs)
        
    