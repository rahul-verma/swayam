
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


from typing import Union

from tarkash import log_debug
from swayam.llm.prompt.types import Perspective, UserPrompt
from swayam.llm.prompt.file import PromptFile
from swayam.llm.expression.expression import LLMExpression
from swayam.llm.expression.repeater import DynamicExpressionFile
from .thought import LLMThought
from swayam.inject.structure.structure import IOStructure

from .format import ThoughtFormatter
from .meta import ThoughtMeta

class Thought(metaclass=ThoughtMeta):
    
    @classmethod
    def expressions(cls, *expressions:LLMExpression, purpose:str=None, perspective:Union[str,Perspective]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMThought:
        if len(expressions) == 0:
            raise ValueError("No expressions provided.")
        out_expressions = []
        for expression in expressions:
            if isinstance (expression, DynamicExpressionFile):
                repeated_expressions = expression.create_expressions()
                out_expressions.extend(repeated_expressions)
            elif isinstance(expression, LLMExpression):
                out_expressions.append(expression)
            else:
                raise ValueError(f"Invalid expression type: {type(expression)}. Should be an LLMExpression or DynamicExpressionFile object.")
            
        if perspective:
            if type(perspective) == str:
                perspective = Perspective(text=perspective)
            elif not isinstance(perspective, Perspective):
                raise ValueError(f"Invalid system prompt type: {type(perspective)}. Should be a string or a Perspective object")
            
        from swayam import Tool, Structure
        if output_structure is not None and type(output_structure) is str:
            output_structure = getattr(Structure, output_structure)
        if tools is not None:
            output_tools = []
            for tool in tools:
                if type(tool) is str:
                    output_tools.append(getattr(Tool, tool))
                else:
                    output_tools.append(tool)
            tools = output_tools
        return LLMThought(*out_expressions, purpose=purpose, perspective=perspective, image=image, output_structure=output_structure, tools=tools)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return ThoughtFormatter(**fmt_kwargs)