
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

class UserExpression:
    
    def __init__(self, *, prompts, purpose:str=None, directive:str=None, image:str=None, output_structure:str=None, tools:list=None, resources=None, before=None, after=None) -> Any:
        self.__prompt_names_or_dicts = list(prompts)
        self.__prompts = []
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Expression"
        else:
            self.__purpose = f"Expression: {self.__purpose}"
        self.__directive = directive
        self.__image = image
        self.__output_structure = output_structure
        self.__tools = tools
        self.__resources = resources
        self.__before = before
        self.__after = after
        
        self.__narrative = None
        
        if self.__output_structure and self.__tools:
            raise ValueError("Cannot suggest both output structure and tools.")
        
    def load(self, *, prompt_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Structure
        from swayam.llm.prompt.namespace import PromptNamespace
            
        for prompt_name_or_dict in self.__prompt_names_or_dicts:
            if isinstance(prompt_name_or_dict, dict):
                prompt_dict = prompt_name_or_dict
                prompt_names = prompt_dict["definitions"]
                generator_structure = Structure.Generator(**prompt_dict["repeater"])
                
                from swayam import Generator
                
                generator = getattr(Generator, generator_structure.generator)

                for out_dict in generator(**generator_structure.args):
                    temp_dict = {}
                    temp_dict.update(fmt_kwargs)
                    temp_dict.update(out_dict)
                    prompt_namespace = PromptNamespace(path=prompt_ns_path, resolution=resolution).formatter(**temp_dict) 
                    for prompt_name in prompt_names:
                        self.__prompts.append(getattr(prompt_namespace, prompt_name))
            else:
                prompt_name = prompt_name_or_dict
                prompt_namespace = PromptNamespace(path=prompt_ns_path, resolution=resolution).formatter(**fmt_kwargs) 
                self.__prompts.append(getattr(prompt_namespace, prompt_name))

        if self.__output_structure:
            self.__output_structure = getattr(Structure, self.__output_structure)
        self.__make_image_suggestions()
        self.__make_structure_suggestions()
        self.__make_tool_suggestions()

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
        
    def append(self, prompt):
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
            if isinstance(prompt, UserExpression):
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
            
    def suggest_tools(self, tools):
        if not self.__tools:
            self.__tools = tools
        self.__make_tool_suggestions()
            