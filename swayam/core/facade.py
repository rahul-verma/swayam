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

import os, sys
from pprint import pprint
import typing

from tarkash import singleton

@singleton
class _SwayamSingleton:
    
    def init(self):  
        from tarkash import Tarkash
        Tarkash.init()      
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
    _Swayam_SINGLETON = None
    
    @classmethod
    def init(cls):
        cls._SWAYAM_SINGLETON = _SwayamSingleton()
        cls._SWAYAM_SINGLETON.init()
        
    @classmethod
    def _get_swayam_res_path(cls, file_name):
        return cls._SWAYAM_SINGLETON.get_swayam_res_path(file_name)
        
    @classmethod
    def execute(cls, *prompts_or_objects, display:bool =True, same_context:bool =True):
        """
        A simple facade to default LLM Model, resulting in one or more prompts being executed.
        
        The goal is to provide an equivalent of a simple web interface like ChatGPT in API-level experience.
        
        The default LLM Model is picked up from configuration.
        
        This method is meant for simple usage where a user wants to execute one or more prompts.
        
        The call supports multiple prompts and other objects to be provided in any sequence. Following are the supported object types:
        1. Prompt as a string.
        2. Prompt as a dictionary with role and content keys.
        3. Prompt as a File. The file names (Text/INI) (or file paths relative to the <ROOT>Prompt directory) can be provided. 
        
        Args:
            *prompts_or_objects (str, List, Dict): The prompts to be executed
            display (bool, optional): If True, the prompts and responses are displayed. Defaults to True.
            same_context (bool, optional): If True, the same context is used for all prompts. Defaults to True.

        Returns:
            (str, List): Returns a string or a list of strings as the output of the LLM.
        """
        from swayam.llm.agent import Agent
        agent = Agent(display=display, report_html=False)
        return agent.execute(*prompts_or_objects, same_context=same_context)