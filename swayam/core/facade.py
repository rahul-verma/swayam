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
from swayam.llm.expression import Expression

@singleton
class _SwayamSingleton:
        
    def get_project_dir(self):
        return self.__project_dir
    
    def __register_config_with_tarkash(self):
        from tarkash import Tarkash
        reg_config = {
            "SNIPPET_DIR": ("definition/snippet", "path"),
            "PROMPT_DIR": ("definition/prompt", "path"),
            "EXPRESSION_DIR": ("definition/expression", "path"),
            "THOUGHT_DIR": ("definition/thought", "path"),
            "STORY_DIR": ("definition/strategy", "path"),
            "LLM_PROVIDER": "openai",
            "LLM_MODEL": "gpt-4o-mini"
        }
        Tarkash.register_framework_config_defaults("swayam", reg_config)
    
    def init(self):   
        from tarkash import Tarkash, TarkashOption
        # Swayam's initialisation depends on Tarkash.init() called  by the creator of the final project using the Traksh based stack of libs.
    
        self.__root_dir = self.__join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
        self.__project_dir = Tarkash.get_option_value(TarkashOption.PROJECT_DIR)
        
        self.__register_config_with_tarkash()
        
        # Create default agent
        from swayam.llm.agent.simple import SimpleAgent
        #print("Creating default agent...")
        self.__default_agent = SimpleAgent(display=True, report_html=False)
    
    def __join_paths(self, *paths):
        return os.path.abspath(os.path.join(*paths))
        
    def run_prompt(self, prompt_text):
        return prompt_text
    
    def get_swayam_root_dir(self):
        return self.__root_dir

    def get_swayam_res_path(self, file_name):
        return self.__join_paths(self.get_swayam_root_dir(), "res", file_name)
    
    @property
    def default_agent(self):
        return self.__default_agent
    
    def agent(self, display=False, report_html=True, run_id=None):
        """
        Creates an Agent.
        
        Args:
            display (bool, optional): If True, the agent will display the console output. Defaults to False.
            report_html (bool, optional): If True, the agent will create a report in HTML format. Defaults to True.
            run_id ([type], optional): The run id for the agent. Defaults to None. The HTML report directory is created with this name and multiple calls to execute with same run_id append results to that report.

        Returns:
            SimpleAgent: A simple agent that executes a parts of or complete strategy.
        """
        from swayam.llm.agent.simple import SimpleAgent
        return SimpleAgent(display=display, report_html=report_html, run_id=run_id)

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
    def enact(cls, prompt:str):
        """
        A simple facade to default LLM Model, resulting in one a prompt being executed.
        
        The goal is to provide a basic chatting experience.
        
        The default LLM Model is picked up from configuration.
        
        This method is meant for simple usage where a user wants to execute one or more prompts.
        
        Args:
            prompt (str): The prompt to be executed

        Returns:
            (str): Returns the message from the LLM.
        """
        if type(prompt) is not str:
            raise TypeError("Prompt should be a string")
        return cls._SWAYAM_SINGLETON.default_agent.enact(prompt)
    
    
    @classmethod
    def agent(cls, display=False, report_html=True, run_id=None):
        """
        Creates an Agent.
        
        Args:
            display (bool, optional): If True, the agent will display the console output. Defaults to False.
            report_html (bool, optional): If True, the agent will create a report in HTML format. Defaults to True.
            run_id ([type], optional): The run id for the agent. Defaults to None. The HTML report directory is created with this name and multiple calls to execute with same run_id append results to that report.

        Returns:
            SimpleAgent: A simple agent that executes a parts of or complete strategy.
        """
        return cls._SWAYAM_SINGLETON.agent(display=display, report_html=report_html, run_id=run_id)