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

from swayam.llm.prompt import Prompt
from tarkash import log_debug
from typing import Any, Union

class SystemPrompt(Prompt):
    
    def __init__(self, *, text:str, image:str=None, tools:list=None ) -> Any:
        super().__init__(role="system", text=text, image=image, tools=tools)

class UserPrompt(Prompt):
    def __init__(self, *, text:str, system_prompt:SystemPrompt=None, image:str=None, tools:list=None) -> Any:
        super().__init__(role="user", text=text, system_prompt=system_prompt, image=image, tools=tools)