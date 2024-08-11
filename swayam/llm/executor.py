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

import os
from pprint import pprint
from tarkash import TarkashObject

class PromptExecutor(TarkashObject):    
    """
    Executes the prompt and returns the result.
    """
    
    def __init__(self, *, model_config, reporter_config, prompt_config):
        tobj_kwargs = dict()
        tobj_kwargs["model_config"] = model_config
        tobj_kwargs["reporter_config"] = reporter_config
        tobj_kwargs["prompt_config"] = prompt_config
        super().__init__(**tobj_kwargs)
        self.__model_config = model_config
        self.__reporter_config = reporter_config
        self.__prompt_config = prompt_config
        self.__client = None
        self.__load()
        
    @property
    def model_config(self):
        return self.__model_config
    
    @property
    def reporter_config(self):
        return self.__reporter_config
    
    @property
    def prompt_config(self):
        return self.__prompt_config
        
    def __load(self):
        from .model import Model
        self.__client = Model.create_client(config=self.model_config, prompt_config=self.prompt_config)
    
    def execute(self, *, prompt_sequence, context, display=True):
        '''
            Runs the prompt text and returns the result.
        '''

        response_messages = []
        messages = []
        
        from swayam.llm.report import PromptSessionHtmlReporter
        
        if self.__reporter_config.enabled:
            reporter = PromptSessionHtmlReporter("session")
        
        for prompt in prompt_sequence:
            
            if display:
                print("-" * 80)
                print("Prompt:")
                print(prompt)
                print("-" * 80)
                
            if display:
                if not context.messages:
                    print("Context Messages: None")
                else:
                    print("Context Messages:")
                    pprint(context.messages)
                print("-" * 80)
                
            context.append_prompt(prompt)
                
            if self.__reporter_config.enabled:
                reporter.report_prompt(prompt)
            
            if self.__reporter_config.enabled:
                reporter.report_context(messages)

            response = self.__client.execute_messages(context.messages)
            response_messages.append(response.choices[0].message)

            if display:
                print("Response:")
                print(response.choices[0].message.content)
            if self.__reporter_config.enabled:
                reporter.report_output(response.choices[0].message)

            context.append_assistant_response(response.choices[0].message.to_dict())
        
        if display:
            print("-"* 80) 
        if self.__reporter_config.enabled:
            if self._show_in_browser:
                reporter.show_in_browser()
        
        return response_messages