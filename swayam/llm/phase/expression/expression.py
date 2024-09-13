
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

def iterator(vault, prompt_names, prompt_ns_path, resolution, driver, driver_kwargs, parent_fmt_kwargs, image, template, actions):
    from swayam.llm.phase.prompt.namespace import PromptNamespace
    for out_dict in driver(vault=vault, **driver_kwargs):
        temp_dict = {}
        temp_dict.update(parent_fmt_kwargs)
        temp_dict.update(out_dict)
        prompt_namespace = PromptNamespace(path=prompt_ns_path, resolution=resolution).formatter(**temp_dict) 
        for prompt_name in prompt_names:
            prompt = getattr(prompt_namespace, prompt_name)
            if image:
                prompt.suggest_image(image)
            if template:
                prompt.suggest_out_template(template)
            if actions:
                prompt.suggest_actions(actions)
            yield prompt

class PromptDriver:
    
    def __init__(self, prompt_dict, *, prompt_ns_path, resolution, parent_fmt_kwargs):
        self.__prompt_ns_path = prompt_ns_path
        self.__resolution = resolution
        self.__parent_fmt_kwargs = parent_fmt_kwargs

        self.__prompt_names = prompt_dict["definitions"]
        from swayam.inject.template.builtin.internal import Driver as DriverTemplate        
        from swayam import Driver
        if isinstance(prompt_dict["driver"], dict):
            driver_data = DriverTemplate(driver=prompt_dict["driver"])        
            self.__driver = getattr(Driver, driver_data.driver.name)
            self.__driver_kwargs = driver_data.driver.args
        else:
            self.__driver = getattr(Driver, prompt_dict["driver"])
            self.__driver_kwargs = dict()
        self.__driver = getattr(Driver, driver_data.driver.name)
        self.__driver_kwargs = driver_data.driver.args
        self.__image = None
        self.__out_template = None
        self.__actions = None
        
    @property
    def vault(self):
        return self.__vault
    
    @vault.setter
    def vault(self, vault):
        self.__vault = vault
        
    def suggest_image(self, image):
        self.__image = image
            
    def suggest_out_template(self, template_name):
        self.__out_template = template_name
            
    def suggest_actions(self, action_names):
        self.__actions = action_names
    
    def __call__(self):
        prompt_loader = iterator(self.__vault, self.__prompt_names, self.__prompt_ns_path, self.__resolution, self.__driver, self.__driver_kwargs, self.__parent_fmt_kwargs, self.__image, self.__out_template, self.__actions)
        return prompt_loader

class UserExpression:
    
    def __init__(self, *, prompts, purpose:str=None, persona:str=None, directive:str=None, image:str=None, out_template:str=None, draft=None, actions:list=None, prologue=None, epilogue=None, prologue_prompt=None, epilogue_prompt=None) -> Any:
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
        self.__out_template = out_template
        self.__actions = actions
        self.__prologue = prologue
        self.__epilogue = epilogue
        self.__prologue_prompt = prologue_prompt
        self.__epilogue_prompt = epilogue_prompt
        self.__story = None
        self.__thought = None
        
        self.__narrative = None
        
        if self.__out_template and self.__actions:
            raise ValueError("Cannot suggest both output structure and actions.")
        
        if draft:
            from swayam import Draft
            from .drafter import Drafter
            self.__draft = getattr(Draft, draft)
            self.__drafter = Drafter(draft_info=self.__draft)
        else:
            self.__drafter = None
        
        from swayam.llm.enact.frame import Frame
        self.__frame = Frame(phase=self, prologue=self.__prologue, epilogue=self.__epilogue)
        self.__prompt_frame = Frame(phase=self, prologue=self.__prologue_prompt, epilogue=self.__epilogue_prompt)
        
    def load(self, *, prompt_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Template
        from swayam.llm.phase.prompt.namespace import PromptNamespace
            
        for prompt_name_or_dict in self.__prompt_names_or_dicts:
            if isinstance(prompt_name_or_dict, dict):
                # Lazy loader of prompts
                prompt_driver = PromptDriver(
                    prompt_name_or_dict["repeat"],
                    prompt_ns_path=prompt_ns_path,
                    resolution=resolution,
                    parent_fmt_kwargs=fmt_kwargs
                )
                self.__prompts.append(prompt_driver)
            else:
                prompt_name = prompt_name_or_dict
                prompt_namespace = PromptNamespace(path=prompt_ns_path, resolution=resolution).formatter(**fmt_kwargs) 
                self.__prompts.append(getattr(prompt_namespace, prompt_name))

        # if self.__out_template:
        #     self.__out_template = getattr(Template, self.__out_template)
        self.__make_image_suggestions()
        self.__make_template_suggestions()
        self.__make_action_suggestions()

    def __make_image_suggestions(self):
        # the image is appended only to the first prompt.
        if self.__image:
            self.__prompts[0].suggest_image(self.__image)
        
    def __make_template_suggestions(self):
        # Actions and response format are suggested to all prompts.            
        for prompt in self.__prompts:
            if self.__out_template:
                prompt.suggest_out_template(self.__out_template)
                
    def __make_action_suggestions(self):
        # Actions and response format are suggested to all prompts.            
        for prompt in self.__prompts:
            if self.__actions:
                prompt.suggest_actions(self.__actions) 
        
    def has_directive(self):
        return self.__directive is not None
    
    @property
    def frame(self):
        return self.__frame
    
    @property
    def drafter(self):
        return self.__drafter
    
    @property
    def prompt_frame(self):
        return self.__prompt_frame
    
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
    def vault(self):
        return self.__vault
    
    @vault.setter
    def vault(self, vault):
        self.__vault = vault.get_phase_wrapper(self)
        self.__vault["purpose"] = self.__purpose
        
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
            
    def suggest_actions(self, actions):
        if not self.__actions:
            self.__actions = actions
        self.__make_action_suggestions()
            