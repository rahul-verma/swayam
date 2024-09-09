
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

def iterator(store, prompt_names, prompt_ns_path, resolution, generator, generator_kwargs, parent_fmt_kwargs):
    from swayam.llm.phase.prompt.namespace import PromptNamespace
    for out_dict in generator(store=store, **generator_kwargs):
        temp_dict = {}
        temp_dict.update(parent_fmt_kwargs)
        temp_dict.update(out_dict)
        prompt_namespace = PromptNamespace(path=prompt_ns_path, resolution=resolution).formatter(**temp_dict) 
        for prompt_name in prompt_names:
            yield getattr(prompt_namespace, prompt_name)

class PromptGenerator:
    
    def __init__(self, prompt_dict, *, prompt_ns_path, resolution, parent_fmt_kwargs):
        self.__prompt_ns_path = prompt_ns_path
        self.__resolution = resolution
        self.__parent_fmt_kwargs = parent_fmt_kwargs

        self.__prompt_names = prompt_dict.pop("definitions")
        from swayam.inject.structure.builtin.internal import Generator as GeneratorStructure
        generator_structure = GeneratorStructure(**prompt_dict)
        
        from swayam import Generator
        self.__generator = getattr(Generator, generator_structure.generator)
        self.__generator_kwargs = generator_structure.args
        
    @property
    def store(self):
        return self.__store
    
    @store.setter
    def store(self, store):
        self.__store = store
    
    def __call__(self):
        prompt_loader = iterator(self.__store, self.__prompt_names, self.__prompt_ns_path, self.__resolution, self.__generator, self.__generator_kwargs, self.__parent_fmt_kwargs)
        return prompt_loader

class UserExpression:
    
    def __init__(self, *, prompts, purpose:str=None, persona:str=None, directive:str=None, image:str=None, output_structure:str=None, tools:list=None, before=None, after=None, before_node=None, after_node=None) -> Any:
        self.__prompt_names_or_dicts = list(prompts)
        self.__prompts = []
        self.__purpose = purpose
        if self.__purpose is None:
            self.__purpose = f"Expression"
        else:
            self.__purpose = f"Expression: {self.__purpose}"
        self.__persona = persona
        self.__directive = directive
        self.__image = image
        self.__output_structure = output_structure
        self.__tools = tools
        self.__before = before
        self.__after = after
        self.__before_node = before_node
        self.__after_node = after_node
        self.__story = None
        self.__thought = None
        
        self.__narrative = None
        
        if self.__output_structure and self.__tools:
            raise ValueError("Cannot suggest both output structure and tools.")
        
        from swayam.llm.enact.fixture import Fixture
        self.__fixture = Fixture(phase=self, before=self.__before, after=self.__after)
        self.__node_fixture = Fixture(phase=self, before=self.__before_node, after=self.__after_node)
        
    def load(self, *, prompt_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Structure
        from swayam.llm.phase.prompt.namespace import PromptNamespace
            
        for prompt_name_or_dict in self.__prompt_names_or_dicts:
            if isinstance(prompt_name_or_dict, dict):
                # Lazy loader of prompts
                prompt_generator = PromptGenerator(
                    prompt_name_or_dict["repeat"],
                    prompt_ns_path=prompt_ns_path,
                    resolution=resolution,
                    parent_fmt_kwargs=fmt_kwargs
                )
                self.__prompts.append(prompt_generator)
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
    def fixture(self):
        return self.__fixture
    
    @property
    def node_fixture(self):
        return self.__node_fixture
    
    @property
    def purpose(self):
        return self.__purpose
    
    @property
    def persona(self):
        return self.__persona
    
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
    def thought(self):
        return self.__thought
    
    @thought.setter
    def thought(self, thought):
        self.__thought = thought
        
    @property
    def store(self):
        return self.__store
    
    @store.setter
    def store(self, store):
        self.__store = store.get_phase_wrapper(self)
        self.__store["purpose"] = self.__purpose
        
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
            