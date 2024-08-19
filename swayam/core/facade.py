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
from swayam.llm.conversation import Conversation

@singleton
class _SwayamSingleton:
        
    def get_project_dir(self):
        return self.__project_dir
    
    def __register_config_with_tarkash(self):
        from tarkash import Tarkash
        reg_config = {
            "STRUCTURE_DIR": ("definition/structure", "path"),
            "TOOL_DIR": ("definition/tool", "path"),
            "PROMPT_DIR": ("definition/prompt", "path"),
            "CONVERSATION_DIR": ("definition/conversation", "path"),
            "TASK_DIR": ("definition/task", "path"),
            "REPORT_DIR": ("report", "path"),
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
        
        # Create default router
        from swayam.llm.router import Router
        #print("Creating default router...")
        self.__default_router = Router(display=True, report_html=False)
    
    def __join_paths(self, *paths):
        return os.path.abspath(os.path.join(*paths))
        
    def run_prompt(self, prompt_text):
        return prompt_text
    
    def get_swayam_root_dir(self):
        return self.__root_dir

    def get_swayam_res_path(self, file_name):
        return self.__join_paths(self.get_swayam_root_dir(), "res", file_name)
    
    @property
    def router(self):
        return self.__default_router

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
    def execute(cls, prompt:str, *, reset_context:bool=False):
        """
        A simple facade to default LLM Model, resulting in one a prompt being executed.
        
        The goal is to provide a basic chatting experience.
        
        The default LLM Model is picked up from configuration.
        
        This method is meant for simple usage where a user wants to execute one or more prompts.
        
        Args:
            prompt (str): The prompt to be executed
            reset_context (bool, optional): If True, the context is reset. Defaults to False (All executions use same context).

        Returns:
            (str): Returns the message from the LLM.
        """
        if type(prompt) is not str:
            raise TypeError("Prompt should be a string")
        from swayam import Prompt
        user_prompt = Prompt.text(prompt)
        return cls._SWAYAM_SINGLETON.router.execute(user_prompt, reset_context=reset_context)