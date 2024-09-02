
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
from swayam.llm.expression.expression import UserExpression
from swayam.llm.prompt.types import Directive
from swayam.llm.expression.conversation import Conversation
from swayam.inject.structure.structure import IOStructure

class UserThought:
    
    def __init__(self, *expressions:UserExpression, purpose:str=None, directive:Directive=None, content:Conversation=None,  image:str=None, output_structure:Union[str, IOStructure]=None, tools:list=None) -> Any:
        self.__expressions = list(expressions)
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = "Thought"
        self.__narrative = None
        self.__directive = directive
           
        for expression in self.__expressions:
            if image:
                expression.suggest_image(image)
                
            if output_structure:
                expression.suggest_output_structure(output_structure)
                
            if tools:
                expression.suggest_tools(tools)
    
    def is_new(self):
        return len(self.__narrative) == 0
        
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
        return self.__narrative
    
    @narrative.setter
    def narrative(self, narrative:Conversation):
        self.__narrative = narrative
        
    def append(self, expression:UserExpression):
        self.__prompts.append(expression)
        
    def __len__(self):
        return len(self.__expressions)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Expression.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Expression (Length: {len(self)})\n"
        
        for expression in self.__expressions:
            description += expression.describe(level + 1)
        
        return description
    
    @property
    def _expressions(self):
        return self.__prompts
        
    def __iter__(self):
        self.__index = -1
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__expressions[self.__index]
        except IndexError:
            self.__index = -1
            raise StopIteration()
        
    def _get_first_child(self):
        return self.__expressions[0]