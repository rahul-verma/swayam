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

import copy
from typing import Union

from tarkash import log_debug
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from swayam.llm.prompt.file import PromptFile
from swayam.llm.expression.expression import LLMExpression
from swayam.inject.structure.structure import IOStructure

class DynamicExpressionFile:
    
    def __init__(self, *, file_name:str, generator):
        self.__file_name = file_name
        self.__generator = generator
        
    def create_expressions(self, **fmt_kwargs):
        from swayam.llm.expression.format import ExpressionFormatter
        out = []
        iterator = iter(self.__generator)
        for data in iterator:
            fmt_dict = copy.deepcopy(fmt_kwargs)
            fmt_dict.update(data)
            out.append(getattr(ExpressionFormatter(**fmt_dict), self.__file_name))
        return out    

class ExpressionFileRepeater:
    
    def __init__(self, *, generator):
        self.__generator = generator
        
    def __getattr__(self, name):
        return DynamicExpressionFile(file_name=name, generator=self.__generator)
        

        
        