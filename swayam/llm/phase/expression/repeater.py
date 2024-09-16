
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


def iterator(iterator_type, expression, prompt_names, prompt_ns_path, resolution, driver, driver_kwargs, parent_fmt_kwargs, image, template, actions):
    from swayam.llm.phase.prompt.namespace import PromptNamespace
    # This is the loop where one input dict is taken for one or more prompt definitions
    for out_dict in driver(phase=expression, **driver_kwargs):
        temp_dict = {}
        temp_dict.update(parent_fmt_kwargs)
        if iterator_type=="draft":
            if "reference_data" in out_dict:
                temp_dict.update(out_dict.pop("reference_data"))
        temp_dict.update(out_dict)
        prompt_namespace = PromptNamespace(path=prompt_ns_path, resolution=resolution).formatter(**temp_dict) 
        
        # This is the loop for an individual prompt definition
        for index, prompt_name in enumerate(prompt_names):
            prompt = getattr(prompt_namespace, prompt_name)
            if iterator_type=="draft":
                if index == 0:
                    prompt.standalone = True
                
            prompt.vault = expression.narrative.vault
            if image:
                prompt.suggest_image(image)
            if template:
                prompt.suggest_out_template(template)
            if actions:
                prompt.suggest_actions(actions)
                
            # Drafting
            if expression.drafter:
                # Is it the last prompt
                if index == len(prompt_names) - 1:
                    prompt.draft_mode = True
                    prompt.out_template = expression.mandatory_out_template
            yield prompt

class PromptDriver:
    
    def __init__(self, expression, prompt_dict, *, primary_key, prompt_ns_path, resolution, parent_fmt_kwargs):
        self.__expression = expression
        self.__primary_key = primary_key
        self.__prompt_ns_path = prompt_ns_path
        self.__resolution = resolution
        self.__parent_fmt_kwargs = parent_fmt_kwargs

        self.__prompt_names = prompt_dict["definitions"]
        self.__standalone = prompt_dict["standalone"]
        from swayam.inject.template.builtin.internal import Driver as DriverTemplate        
        from swayam import Driver
        
        if self.__primary_key == "repeat":
            self.__iterator_type = "repeat"
            if isinstance(prompt_dict["driver"], dict):
                driver_data = DriverTemplate(driver=prompt_dict["driver"])        
                self.__driver = getattr(Driver, driver_data.driver.name)
                self.__driver_kwargs = driver_data.driver.args
            else:
                self.__driver = getattr(Driver, prompt_dict["driver"])
                self.__driver_kwargs = dict()
        else:
            # It is "draft"
            self.__iterator_type = "draft"
            from swayam.inject.driver.builtin.internal.DraftLooper import DraftLooper
            self.__driver = DraftLooper
            self.__driver_kwargs = {"entity_name": prompt_dict["artifact"]}
        self.__image = None
        self.__out_template = None
        self.__actions = None
        
    def suggest_image(self, image):
        self.__image = image
            
    def suggest_out_template(self, template_name):
        self.__out_template = template_name
            
    def suggest_actions(self, action_names):
        self.__actions = action_names
        
    @property
    def is_standalone(self):
        return self.__standalone
    
    def __call__(self):
        prompt_loader = iterator(self.__iterator_type, self.__expression, self.__prompt_names, self.__prompt_ns_path, self.__resolution, self.__driver, self.__driver_kwargs, self.__parent_fmt_kwargs, self.__image, self.__out_template, self.__actions)
        return prompt_loader