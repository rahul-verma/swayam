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
from swayam.llm.expression.narrative import ExpressionNarrative
from swayam.llm.prompt.prompt import UserPrompt
from swayam.llm.enactor.prompt import PromptEnactor

class PromptNarrator:

    def __init__(self, display=False, record_html=True, narration=None):
        from swayam.llm.config.report import RecorderConfig
        self.__recorder_config = RecorderConfig(display=display, record_html=record_html)
        
        if not narration:
            self.__recorder_config._narration = datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.__recorder_config._narration = str(narration)
            
        from swayam.llm.record.recorder import Recorder
        log_debug(f"Creating Listener")
        self.__recorder = Recorder(self.__recorder_config)
        log_debug("Narrator initialized.")
        
        self.__narrative = ExpressionNarrative()
    
    def enact(self, prompt):
        """
        Executes a prompt text.
        """
        if not isinstance(prompt, UserPrompt):
            raise TypeError(f"PromptNarrator cannot execute prompt of type {type(prompt)}. It must UserPrompt object.")
        
        log_debug(f"Executing prompt.")
        enactor = PromptEnactor(recorder=self.__recorder)
        enactor.enact(prompt, narrative=self.__narrative)
        self.__recorder.finish()
        
    def reset(self):
        self.__narrative = ExpressionNarrative()
        self.__recorder.reset()