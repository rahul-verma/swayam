
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

from typing import Any, Union

from tarkash import log_debug
from swayam.llm.prompt import Prompt
from swayam.llm.prompt.types import Directive, UserPrompt
from ...swayam.llm.expression.narrative import ExpressionNarrative
from swayam.inject.structure.structure import IOStructure

class LLMExpression:
    
    def __init__(self, *prompts:Prompt, purpose:str=None, directive:Directive=None, narrative:ExpressionNarrative=None,  image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None, standalone:bool=False, reset_narrative:bool=True, store_response_as:str=None) -> Any:
        self.__prompts = list(prompts)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Expression"
        self.__narrator_narrative = narrative
        self.__directive = directive
        self.__image = image
        self.__output_structure = output_structure
        self.__tools = tools
        self.__store_response_as = store_response_as
        self.__make_image_suggestions()
        self.__make_structure_suggestions()
        self.__make_tool_suggestions()
        
        # Depends on how it was created. When it is a single prompt expression created for an execute call of Narrator, it is treated as a continuation of the previous expression.
        self.__extends_previous_expression = False
        
        # If True, it gets an empty narrative value. Has no impact on narrative of the follow-up expressions.
        self.__standalone = standalone
        
        # If True, it resets the parent's narrative for itself. The subsequent expression receives the narrative that it results in.
        self.__reset_narrative = reset_narrative
        
    @property
    def should_store_response(self):
        return self.__store_response_as is not None
    
    @property
    def response_storage_name(self):
        return self.__store_response_as
        
    @property
    def standalone(self):
        return self.__standalone
    
    @property
    def reset_narrative(self):
        return self.__reset_narrative
        
    @property
    def extends_previous_expression(self):
        return self.__extends_previous_expression
    
    @extends_previous_expression.setter
    def extends_previous_expression(self, value:bool):
        self.__extends_previous_expression = value
        
    @property
    def extends_previous_expression(self):
        return self.__extends_previous_expression
    
    @extends_previous_expression.setter
    def extends_previous_expression(self, value:bool):
        self.__extends_previous_expression = value

    def __make_image_suggestions(self):
        # the image is appended only to the first prompt.
        if self.__image:
            self.__prompts[0].suggest_image(self.__image)
        
    def __make_structure_suggestions(self):
        # Tools and response format are suggested to all prompts.            
        for prompt in self.__prompts:
            if self.__image:
                prompt.suggest_output_structure(self.__output_structure)
                
    def __make_tool_suggestions(self):
        # Tools and response format are suggested to all prompts.            
        for prompt in self.__prompts:
            if self.__tools:
                prompt.suggest_tools(self.__tools) 
    
    def is_new(self):
        return len(self.__narrator_narrative.expression_narrative) == 0
        
    def has_directive(self):
        return self.__directive is not None
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def directive(self):
        return self.__directive
        
    @directive.setter
    def directive(self, directive:Directive):
        self.__directive = directive
        
    @property
    def narrative(self):
        return self.__narrator_narrative
    
    @narrative.setter
    def narrative(self, narrative:ExpressionNarrative):
        self.__narrator_narrative = narrative
        
    def append(self, prompt:Prompt):
        self.__prompts.append(prompt)
        
    def __len__(self):
        return len(self.__prompts)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Expression.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Expression (Length: {len(self)})\n"
        
        for prompt in self.__prompts:
            if isinstance(prompt, LLMExpression):
                description += prompt.describe(level + 1)
            else:
                description += f"{indent}  {type(prompt).__name__}\n"
        
        return description
    
    @property
    def _prompts(self):
        return self.__prompts
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__prompts[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
        
    def _get_first_child(self):
        return self.__prompts[0]
    

    def suggest_image(self, image):
        if not self.__image:
            self.__image = image
        self.__make_image_suggestions()
            
    def suggest_output_structure(self, output_structure):
        if not self.__output_structure:
            self.__output_structure = output_structure
        self.__make_structure_suggestions()
            
    def suggest_tools(self, tools):
        if not self.__tools:
            self.__tools = tools
        self.__make_tool_suggestions()
            