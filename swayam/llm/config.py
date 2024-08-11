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

class ModelConfig:

    def __init__(self, *, provider, model):
        from tarkash import Tarkash
        from swayam.core.constant import SwayamOption
        provider = provider or Tarkash.get_option_value(SwayamOption.LLM_PROVIDER)
        model = model or Tarkash.get_option_value(SwayamOption.LLM_MODEL)
        self._provider = provider
        self._model = model
        
    @property
    def provider(self):
        return self._provider
    
    @property
    def model(self):
        return self._model
    
class ReporterConfig:

    def __init__(self, *, enabled, show_in_browser):
        self._enabled = enabled
        self._show_in_browser = show_in_browser
        
    @property
    def enabled(self):
        return self._enabled
    
    @property
    def show_in_browser(self):
        return self._show_in_browser


class PromptConfig:
    
    def __init__(self, *, temperature=0, **kwargs):
        self._model_kwargs = dict()
        self._model_kwargs["temperature"] = temperature

    @property
    def model_kwargs(self):
        return self._model_kwargs
    
    @property
    def temperature(self):
        return self._model_kwargs["temperature"]
        
    