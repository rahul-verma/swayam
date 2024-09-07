
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

class UserThought:
    
    def __init__(self, *, expressions, purpose:str=None, directive:str=None, tools:list=None, resources=None, before=None, after=None, before_node=None, after_node=None) -> Any:
        self.__expression_names_or_dicts = list(expressions)
        self.__expressions = []
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Thought"
        else:
            self.__purpose = f"Thought: {self.__purpose}"
        self.__directive = directive
        self.__tools = tools
        self.__before = before
        self.__after = after
        self.__before_node = before_node
        self.__after_node = after_node
        self.__story = None
        
        self.__narrative = None
        
    def load(self, *, expression_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Structure
        from swayam.llm.phase.expression.namespace import ExpressionNamespace
        for expression_name_or_dict in self.__expression_names_or_dicts:
            if isinstance(expression_name_or_dict, dict):
                expression_dict = expression_name_or_dict["repeat"]
                expression_names = expression_dict.pop("definitions")
                from swayam.inject.structure.builtin.internal import Generator as GeneratorStructure
                generator_structure = GeneratorStructure(**expression_dict)
                
                from swayam import Generator
                
                generator = getattr(Generator, generator_structure.generator)

                for out_dict in generator(**generator_structure.args):
                    temp_dict = {}
                    temp_dict.update(fmt_kwargs)
                    temp_dict.update(out_dict)
                    expression_namespace = ExpressionNamespace(path=expression_ns_path, resolution=resolution).formatter(**temp_dict) 
                    for expression_name in expression_names:
                        expression = getattr(expression_namespace, expression_name)
                        self.__expressions.append(expression)
            else:
                expression_name = expression_name_or_dict
                expression_namespace = ExpressionNamespace(path=expression_ns_path, resolution=resolution).formatter(**fmt_kwargs) 
                self.__expressions.append(getattr(expression_namespace, expression_name))
        self.__make_tool_suggestions()
                
    def __make_tool_suggestions(self):
        # Tools and response format are suggested to all expressions.            
        for expression in self.__expressions:
            if self.__tools:
                expression.suggest_tools(self.__tools) 
        
    def has_directive(self):
        return self.__directive is not None
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def directive(self):
        return self.__directive
        
    @directive.setter
    def directive(self, directive):
        self.__directive = directive
        
    @property
    def narrative(self):
        return self.__narrative
    
    @narrative.setter
    def narrative(self, narrative):
        self.__narrative = narrative
        
    @property
    def story(self):
        return self.__story
    
    @story.setter
    def story(self, story):
        self.__story = story
        
    @property
    def store(self):
        return self.__store
    
    @store.setter
    def store(self, store):
        self.__store = store.get_phase_wrapper(self)
        self.__store["purpose"] = self.__purpose
        
    def __len__(self):
        return len(self.__expressions)
        
    def describe(self, level=0):
        """
        Returns a string describing the structure of the Expression.
        Includes the length and a tree representation of the contained objects.
        """
        indent = " " * level
        description = f"{indent}Thought (Length: {len(self)})\n"
        
        for expression in self.__expressions:
            description += expression.describe(level + 1)
        
        return description
    
    @property
    def _expressions(self):
        return self.__expressions
        
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
            