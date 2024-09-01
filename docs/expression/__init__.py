
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
from swayam.llm.prompt.types import Directive, UserPrompt
from swayam.llm.prompt.file import PromptFile
from .format import ExpressionFormatter
from .expression import LLMExpression
from swayam.inject.structure.structure import IOStructure
from .meta import ExpressionMeta

class Expression(metaclass=ExpressionMeta):
    
    @classmethod
    def prompts(cls, *prompts:UserPrompt, purpose:str=None, directive:Union[str,Directive]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_narrative:bool=True, store_response_as:str=None) -> LLMExpression:
        if len(prompts) == 0:
            raise ValueError("No prompts provided.")
        for prompt in prompts:
            if not isinstance(prompt, UserPrompt):
                raise ValueError(f"Invalid prompt type: {type(prompt)}. Should be a UserPrompt object.")
        if directive:
            if type(directive) == str:
                directive = Directive(text=directive)
            elif not isinstance(directive, Directive):
                raise ValueError(f"Invalid system prompt type: {type(directive)}. Should be a string or a Directive object")
            
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

        return LLMExpression(*prompts, purpose=purpose, directive=directive, image=image, output_structure=output_structure, tools=tools, reset_narrative=reset_narrative, standalone=standalone, store_response_as=store_response_as)
    
    @classmethod
    def texts(cls, *prompts:UserPrompt, purpose:str=None, directive:Union[str,Directive]=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_narrative:bool=True, store_response_as:str=None) -> LLMExpression:
        for prompt in prompts:
            if type(prompt) is not str:
                raise ValueError(f"Invalid prompt type: {type(prompt)}. Should be a string")
        return cls.prompts(*[UserPrompt(text=prompt) for prompt in prompts], purpose=purpose, directive=directive,  image=image, output_structure=output_structure, tools=tools, reset_narrative=reset_narrative, standalone=standalone, store_response_as=store_response_as)
    
    @classmethod
    def formatter(self, **fmt_kwargs):
        return ExpressionFormatter(**fmt_kwargs)