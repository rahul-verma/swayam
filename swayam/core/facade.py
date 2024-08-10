# This file is a part of Tarkash
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

import os, sys
from pprint import pprint
import typing
from tarkash.core.adv.decorator import singleton

@singleton
class _SwayamSingleton:
    
    def init(self):        
        self.__root_dir = self.__join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
    
    def __join_paths(self, *paths):
                return os.path.abspath(os.path.join(*paths))
        
    def run_prompt(self, prompt_text):
        return prompt_text
    
    def get_swayam_root_dir(self):
        return self.__root_dir

    def get_swayam_res_path(self, file_name):
        return self.__join_paths(self.get_swayam_root_dir(), "res", file_name)

class Swayam:
    '''
        Swayam is the facade of Swayam framework.
        Contains static methods which wrapper an internal singleton class for easy access to top-level Swayam functions.
    '''
    _TARKASH_SINGLETON = None
    
    @classmethod
    def init(cls):
        cls._SWAYAM_SINGLETON = _SwayamSingleton()
        cls._SWAYAM_SINGLETON.init()
        
    @classmethod
    def _get_swayam_res_path(cls, file_name):
        return cls._SWAYAM_SINGLETON.get_swayam_res_path(file_name)
        
    @classmethod
    def run_prompt(cls, *prompts_or_objects, model="gpt-4o-mini", temperature=0, content_only=True, display=True, report_html=False, show_in_browser=True, **kwargs):
        '''
            Runs the prompt text and returns the result.
        '''
        from openai import OpenAI
        from swayam.prompt.source import PromptTextFile, PromptIniFile
        prompts = []
        
        for prompt_or_object in prompts_or_objects:
            if isinstance(prompt_or_object, PromptTextFile):
                prompts.append(prompt_or_object.content)
            elif isinstance(prompt_or_object, PromptIniFile):
                prompts.extend(prompt_or_object.content.values())
            elif isinstance(prompt_or_object, str):
                if prompt_or_object.lower().endswith('.txt'):
                    prompts.append(PromptTextFile(prompt_or_object).content)
                elif prompt_or_object.lower().endswith('.ini'):
                    prompts.extend(PromptIniFile(prompt_or_object).content.values())
                else:
                    prompts.append(prompt_or_object)
            else:
                raise TypeError(f"Invalid type for prompt: {type(prompt_or_object)}")
    
        
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        
        contents_or_messages = []
        messages = []
        
        from swayam.report.html import PromptSessionHtmlReporter
        
        if report_html:
            reporter = PromptSessionHtmlReporter("session")
        
        for prompt in prompts:
            if display:
                print("-" * 80)
                print("Prompt:")
                print(prompt)
                print("-" * 80)
                
            if report_html:
                reporter.report_prompt(prompt)
                
            messages.extend([{"role": "user", "content": prompt}])
            
            if report_html:
                reporter.report_context(messages)

            if display:
                print("Messages:")
                pprint(messages)
                print("-" * 80)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature, # this is the degree of randomness of the model's output
                **kwargs
            )
            content = response.choices[0].message.content
            if content_only:
                contents_or_messages.append(content)
            else:
                message = response.choices[0].message
                contents_or_messages.append(message)

            if display:
                print("Response:")
                print(content)
            if report_html:
                reporter.report_output(response.choices[0].message)

            messages.extend([response.choices[0].message.to_dict()])
        
        if display:
            print("-"* 80) 
        if report_html:
            if show_in_browser:
                reporter.show_in_browser()
        
        if len(contents_or_messages) == 1:
            return contents_or_messages[0]     
        return contents_or_messages