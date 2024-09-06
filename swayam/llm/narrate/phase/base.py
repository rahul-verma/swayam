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

from abc import ABC, abstractmethod


from datetime import datetime
from tarkash import log_debug
from swayam.llm.phase.prompt.prompt import UserPrompt
from swayam.llm.enact.prompt import PromptEnactor
from .narrative import Narrative

class BaseNarrator(ABC):

    def __init__(self, display=False, record_html=True, narration=None):
        from swayam.llm.config.recorder import RecorderConfig
        self.__recorder_config = RecorderConfig(display=display, record_html=record_html)
        
        if not narration:
            self.__recorder_config._narration = datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.__recorder_config._narration = str(narration)
            
        from swayam.llm.record.recorder import Recorder
        log_debug(f"Creating Recorder")
        self.__recorder = Recorder(self.__recorder_config)
        log_debug("Narrator initialized.")
        
        self.__narrative = Narrative()
        
    @property
    def narrative(self):
        return self.__narrative
    
    @property
    def recorder(self):
        return self.__recorder
    
    @abstractmethod
    def narrate(self, phase):
        """
        Narrates a phase in STEP.
        """
        pass
        
    def finish(self):
        self.__recorder.finish()
        
    def reset(self):
        self.__narrative = Narrative()
        self.__recorder.reset()
