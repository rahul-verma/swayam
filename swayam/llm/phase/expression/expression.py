
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
        self.__drafter = None
        
        if self.__out_template and self.__actions:
            raise ValueError("Cannot suggest both output template and actions.")
        
        from swayam.llm.enact.frame import Frame
        self.__frame = Frame(phase=self, prologue=self.__prologue, epilogue=self.__epilogue)
        self.__prompt_frame = Frame(phase=self, prologue=self.__prologue_prompt, epilogue=self.__epilogue_prompt)
        
    def load(self, *, prompt_ns_path, resolution=None, **fmt_kwargs):
        from swayam import Template
        from swayam.llm.phase.prompt.namespace import PromptNamespace
            
        for prompt_name_or_dict in self.__prompt_names_or_dicts:
            if isinstance(prompt_name_or_dict, dict):
                from .repeater import PromptDriver
                prompt_dict = None
                primary_key = None
                if "repeat" in prompt_name_or_dict:
                    prompt_dict = prompt_name_or_dict["repeat"]
                    primary_key = "repeat"
                elif "draft" in prompt_name_or_dict:
                    prompt_dict = prompt_name_or_dict["draft"]
                    primary_key = "draft"
                else:
                    raise ValueError("Prompt dictionary must have a 'repeat' or 'draft' key.")
                # Lazy loader of prompts
                prompt_driver = PromptDriver(
                    self,
                    prompt_dict,
                    primary_key=primary_key,
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
    
    @drafter.setter
    def drafter(self, drafter):
        self.__drafter = drafter
    
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
        Returns a string describing the template of the Expression.
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
            