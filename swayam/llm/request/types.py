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

from .base import BaseRequest
from tarkash import log_debug
from typing import Any, Union
from swayam.inject.structure.structure import IOStructure

class SystemRequest(BaseRequest):
    
    def __init__(self, *, text:str) -> Any:
        super().__init__(role="system", text=text)

class UserRequest(BaseRequest):
    def __init__(self, *, text:str, purpose:str=None, image:str=None, output_structure:IOStructure=None, tools:list=None) -> Any:
        super().__init__(role="user", text=text, purpose=purpose, image=image, output_structure=output_structure, tools=tools)