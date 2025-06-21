
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

def iterator(vault, expression_names, expression_ns_path, resolution, driver, driver_kwargs, parent_fmt_kwargs, actions):
    from swayam.llm.phase.expression.namespace import ExpressionNamespace
    for out_dict in driver(vault=vault, **driver_kwargs):
        temp_dict = {}
        temp_dict.update(parent_fmt_kwargs)
        temp_dict.update(out_dict)
        expression_namespace = ExpressionNamespace(path=expression_ns_path, resolution=resolution).formatter(**temp_dict) 
        for expression_name in expression_names:
            expression = getattr(expression_namespace, expression_name)
            if actions:
                expression.suggest_actions(actions)
            yield expression

class ExpressionDriver:
    
    def __init__(self, expression_dict, *, expression_ns_path, resolution, parent_fmt_kwargs):
        self.__expression_ns_path = expression_ns_path
        self.__resolution = resolution
        self.__parent_fmt_kwargs = parent_fmt_kwargs

        self.__expression_names = expression_dict["definitions"]
        from swayam.inject.template.builtin.internal import Driver as DriverTemplate
        from swayam import Driver
        if isinstance(expression_dict["driver"], dict):
            driver_data = DriverTemplate(driver=expression_dict["driver"])        
            self.__driver = getattr(Driver, driver_data.driver.name)
            self.__driver_kwargs = driver_data.driver.args
        else:
            self.__driver = getattr(Driver, expression_dict["driver"])
            self.__driver_kwargs = dict()
        self.__actions = None
        
    @property
    def vault(self):
        return self.__vault
    
    @vault.setter
    def vault(self, vault):
        self.__vault = vault
        
    def suggest_actions(self, action_names):
        self.__actions = action_names
    
    def __call__(self):
        expression_loader = iterator(self.__vault, self.__expression_names, self.__expression_ns_path, self.__resolution, self.__driver, self.__driver_kwargs, self.__parent_fmt_kwargs, self.__actions)
        return expression_loader

class UserThought:
    
    def __init__(self, *, name, expressions, purpose:str=None, directive:str=None, actions:list=None, resources=None, prologue=None, epilogue=None) -> Any:
        self.__name = name
        self.__expression_names_or_dicts = list(expressions)
        self.__expressions = []
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Thought"
        else:
            self.__purpose = f"Thought: {self.__purpose}"
        self.__directive = directive
        self.__actions = actions
        self.__prologue = prologue
        self.__epilogue = epilogue
        self.__story = None
        
        self.__narrative = None
        
        from swayam.llm.enact.frame import Frame
        self.__frame = Frame(phase=self, prologue=self.__prologue, epilogue=self.__epilogue)
        
    def load(self, *, expression_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Template
        from swayam.llm.phase.expression.namespace import ExpressionNamespace
        for expression_name_or_dict in self.__expression_names_or_dicts:
            if isinstance(expression_name_or_dict, dict):
                # Lazy loader of prompts
                expression_driver = ExpressionDriver(
                    expression_name_or_dict["repeat"],
                    expression_ns_path=expression_ns_path,
                    resolution=resolution,
                    parent_fmt_kwargs=fmt_kwargs
                )
                self.__expressions.append(expression_driver)
            else:
                expression_name = expression_name_or_dict
                expression_namespace = ExpressionNamespace(path=expression_ns_path, resolution=resolution).formatter(**fmt_kwargs) 
                self.__expressions.append(getattr(expression_namespace, expression_name))
        self.__make_action_suggestions()
                
    def __make_action_suggestions(self):
        # Actions and response format are suggested to all expressions.            
        for expression in self.__expressions:
            if self.__actions:
                expression.suggest_actions(self.__actions) 
        
    def has_directive(self):
        return self.__directive is not None
    
    @property
    def name(self):
        return self.__name
    
    @property
    def frame(self):
        return self.__frame
    
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
    def vault(self):
        return self.__vault
    
    @vault.setter
    def vault(self, vault):
        self.__vault = vault.get_phase_wrapper(self)
        self.__vault["purpose"] = self.__purpose
        
    def __len__(self):
        return len(self.__expressions)
        
    def describe(self, level=0):
        """
        Returns a string describing the template of the Expression.
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
            