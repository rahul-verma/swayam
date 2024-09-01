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

from swayam.llm.expression.file import ExpressionFile
from swayam.llm.expression.expression import LLMExpression
from swayam.llm.prompt.file import PromptFile
from swayam.llm.prompt.types import SystemPrompt, UserPrompt
from swayam.llm.prompt.format import PromptFormatter
from swayam.inject.structure.structure import IOStructure

class ThoughtFormatter:
    
    def __init__(self, **fmt_kwargs):
        self.__fmt_kwargs = fmt_kwargs

    def expression_files(self, *expression_files:ExpressionFile, purpose:str=None, system_prompt:PromptFile=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> LLMExpression:
        from swayam.llm.expression.format import ExpressionFormatter
        from swayam.llm.expression.repeater import DynamicExpressionFile
        
        if len(expression_files) == 0:
            raise ValueError("No expressions provided.")
        expressions = []
        for expression_file in expression_files:
            if isinstance (expression_file, DynamicExpressionFile):
                out_expressions = expression_file.create_expressions(**self.__fmt_kwargs)
                expressions.extend(out_expressions)
            elif isinstance(expression_file, ExpressionFile):
                formatter = ExpressionFormatter(**self.__fmt_kwargs)
                expression = getattr(formatter, expression_file.file_name)
                expressions.append(expression)
            else:
                raise ValueError(f"Invalid expression type: {type(expression_file)}. Should be a ExpressionFile object.") 
            
        if system_prompt:
            if not isinstance(system_prompt, PromptFile) and not isinstance(system_prompt, SystemPrompt):
                raise ValueError(f"Invalid system prompt type: {type(system_prompt)}. Should be a SystemPrompt or PromptFile object.")  
            elif not system_prompt.role == "system":
                raise ValueError(f"Invalid prompt role: {system_prompt.role}. Should be a system prompt.")
            
            if isinstance(system_prompt, PromptFile):
                system_formatter = PromptFormatter(role=system_prompt.role, **self.__fmt_kwargs)
                system_prompt = getattr(system_formatter, system_prompt.file_name)
                if not isinstance(system_prompt, SystemPrompt):
                    raise ValueError(f"There has been a critical framework issue in creating a system prompt.")
            else:
                # If a system prompt is provided directly, it is NOT formatted.
                pass

        from swayam import Thought
        return Thought.expressions(*expressions, purpose=purpose, system_prompt=system_prompt, image=image, output_structure=output_structure, tools=tools)
    
    def __getattr__(self, name):
        from .namespace import ThoughtDir
        import yaml
        with open(ThoughtDir.get_path_for_thought(name=name), "r", encoding="utf-8") as f:
            content = yaml.safe_load(f.read().format(**self.__fmt_kwargs))
        return ThoughtDir.create_thought_from_content(name, content, **self.__fmt_kwargs)