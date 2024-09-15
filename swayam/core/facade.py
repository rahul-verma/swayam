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
        
    def get_project_dir(self):
        return self.__project_dir
    
    def __register_config_with_tarkash(self, folio_dir):
        from tarkash import Tarkash
        reg_config = {
            "EPIC_DIR": ("", "project_relative_path"),
            "DEFINITION_SNIPPET_DIR": ("definition/snippet", "project_relative_path"),
            "DEFINITION_PROMPT_DIR": ("definition/prompt", "project_relative_path"),
            "DEFINITION_EXPRESSION_DIR": ("definition/expression", "project_relative_path"),
            "DEFINITION_THOUGHT_DIR": ("definition/thought", "project_relative_path"),
            "DEFINITION_STORY_DIR": ("definition/story", "project_relative_path"),
            "DEFINITION_ARTIFACT_DIR": ("definition/artifact", "project_relative_path"),
            "FOLIO_DIR": (folio_dir, "absolute_path"),
            "FOLIO_NARRATION_DIR": (os.path.join(folio_dir, "narration"), "absolute_path"),
            "FOLIO_DRAFT_DIR": (os.path.join(folio_dir, "draft"), "absolute_path"),
            "FOLIO_TRANSLATION_DIR": (os.path.join(folio_dir, "translation"), 
                                      "absolute_path"),
            "FOLIO_ARTIFACT_DIR": (os.path.join(folio_dir, "artifact"), 
                                      "absolute_path"),
            "LOG_DIR": (os.path.join(folio_dir, "log"), "absolute_path"),
            "LLM_PROVIDER": "openai",
            "LLM_MODEL": "gpt-4o-mini"
        }
        Tarkash.register_framework_config_defaults("swayam", reg_config)
    
    def init(self, folio_dir=None):   
        from tarkash import Tarkash, TarkashOption
        # Swayam's initialisation depends on Tarkash.init() called  by the creator of the final project using the Traksh based stack of libs.
    
        self.__root_dir = self.__join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
        self.__project_dir = Tarkash.get_option_value(TarkashOption.PROJECT_DIR)
        
        try:
            final_folio_dir = os.environ["FOLIO_DIR"]
        except KeyError:
            if folio_dir is None:
                final_folio_dir =os.path.join(self.__project_dir, "folio")
            else:
                final_folio_dir = folio_dir
        
        self.__register_config_with_tarkash(final_folio_dir)
        
        # Create default narrator
        from swayam.llm.narrate.simple import SimpleNarrator
        #print("Creating default narrator...")
        self.__default_narrator = SimpleNarrator()
    
    def __join_paths(self, *paths):
        return os.path.abspath(os.path.join(*paths))
        
    def run_prompt(self, prompt_text):
        return prompt_text
    
    def get_swayam_root_dir(self):
        return self.__root_dir

    def get_swayam_res_path(self, file_name):
        return self.__join_paths(self.get_swayam_root_dir(), "res", file_name)
    
    @property
    def default_narrator(self):
        return self.__default_narrator
    
    def narrator(self, display=False, record_html=True, narration=None):
        """
        Creates an Narrator.
        
        Args:
            display (bool, optional): If True, the narrator will display the console output. Defaults to False.
            record_html (bool, optional): If True, the narrator will create a report in HTML format. Defaults to True.
            narration ([type], optional): The run id for the narrator. Defaults to None. The HTML report directory is created with this name and multiple calls to execute with same narration append results to that report.

        Returns:
            SimpleNarrator: A simple narrator that executes a parts of or complete story.
        """
        from swayam.llm.narrate.prompt import SimpleNarrator
        return SimpleNarrator(display=display, record_html=record_html, narration=narration)
    
    def reset_narrator(self):
        """
        Resets the default narrator.
        """
        from swayam.llm.narrate.simple import SimpleNarrator
        self.__default_narrator.reset()
        
class SwayamMeta(type):
    
    def __getattr__(cls, name):
        from swayam.llm.narrate import Narrator
        if name == "narrator":
            return Narrator()

class Swayam(metaclass=SwayamMeta):
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
    def narrate(cls, prompt:str):
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
        return cls._SWAYAM_SINGLETON.default_narrator.narrate(prompt)
    
    @classmethod
    def reset_narrator(cls):
        """
        Resets the default narrator.
        """
        cls._SWAYAM_SINGLETON.reset_narrator()