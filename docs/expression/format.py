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

from swayam.llm.prompt.file import PromptFile
from swayam.llm.prompt.types import Directive, UserPrompt
from swayam.llm.prompt.format import PromptFormatter
from .expression import UserExpression
from swayam.inject.structure.structure import IOStructure

class ExpressionFormatter:
    
    def __init__(self, **fmt_kwargs):
        self.__fmt_kwargs = fmt_kwargs

    def prompt_files(self, *prompt_files:PromptFile, purpose:str=None, directive:PromptFile=None, image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_narrative:bool=True, store_response_as:str=None) -> UserExpression:
        if len(prompt_files) == 0:
            raise ValueError("No prompts provided.")
        prompts = []
        for prompt_file in prompt_files:
            if not isinstance(prompt_file, PromptFile):
                raise ValueError(f"Invalid prompt type: {type(prompt_file)}. Should be a PromptFile object.")  
            
            formatter = PromptFormatter(role=prompt_file.role, **self.__fmt_kwargs)
            prompt = getattr(formatter, prompt_file.file_name)
            prompts.append(prompt)
            
        if directive:
            if not isinstance(directive, PromptFile) and not isinstance(directive, Directive):
                raise ValueError(f"Invalid system prompt type: {type(directive)}. Should be a Directive or PromptFile object.")  
            elif not directive.role == "system":
                raise ValueError(f"Invalid prompt role: {directive.role}. Should be a system prompt.")
            
            if isinstance(directive, PromptFile):
                system_formatter = PromptFormatter(role=directive.role, **self.__fmt_kwargs)
                directive = getattr(system_formatter, directive.file_name)
                if not isinstance(directive, Directive):
                    raise ValueError(f"There has been a critical framework issue in creating a system prompt.")
            else:
                # If a system prompt is provided directly, it is NOT formatted.
                pass
        
        from swayam import Expression
        return Expression.prompts(*prompts, purpose=purpose, directive=directive, image=image, output_structure=output_structure, tools=tools, reset_narrative=reset_narrative, standalone=standalone, store_response_as=store_response_as)
    
    def __getattr__(self, name):
        from .namespace import ExpressionDir
        import yaml
        with open(ExpressionDir.get_path_for_expression(name=name)) as f:
            content = yaml.safe_load(f.read().format(**self.__fmt_kwargs))
        return ExpressionDir.create_expression_from_content(name, content, **self.__fmt_kwargs)