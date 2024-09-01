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

from datetime import datetime
from tarkash import log_debug
from .narrative import NarratorNarrative

class SimpleNarrator:
    
    def __init__(self):
        self.__narrative = NarratorNarrative()
        from swayam.llm.config.report import RecorderConfig
        self.__recorder_config = RecorderConfig(display=True, record_html=False)
            
        from swayam.llm.record.recorder import Recorder
        log_debug(f"Creating Listener")
        self.__recorder = Recorder(self.__recorder_config)
        log_debug("Narrator initialized.")
    
    def enact(self, prompt):
        """
        Executes a prompt text.
        """
        
        if not isinstance(prompt, str):
            raise TypeError(f"Simple Narrator cannot execute prompt of type {type(prompt)}. It must be a string.")
        
        from swayam.llm.prompt.types import UserPrompt
        from swayam.llm.enactor.prompt import PromptEnactor
        log_debug(f"Executing prompt.")
        enactor = PromptEnactor(recorder=self.__recorder)
        enactor.enact(UserPrompt(text=prompt))
        self.__recorder.finish()