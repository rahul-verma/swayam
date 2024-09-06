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

from tarkash import log_debug
from swayam.llm.phase.prompt.prompt import UserPrompt
from swayam.llm.enact.prompt import PromptEnactor

from .base import BaseNarrator

class PromptNarrator(BaseNarrator):

    def __init__(self, display=False, record_html=True, narration=None):
        super().__init__(display=display, record_html=record_html, narration=narration)
        self.__first_prompt = True
    
    def narrate(self, prompt):
        """
        Narrates a prompt to a Prompt enactor.
        """
        if self.__first_prompt:
            self.narrative.conversation.append_directive(self.narrative._prepare_directive(expression_directive=None, expression_persona=None))
            self.__first_prompt = False
            
        if not isinstance(prompt, UserPrompt):
            raise TypeError(f"PromptNarrator cannot narrate a prompt of type {type(prompt)}. It must UserPrompt object.")
        
        log_debug(f"Narrating prompt....")
        enactor = PromptEnactor(recorder=self.recorder)
        enactor.enact(prompt, narrative=self.narrative)
        
    def reset(self):
        super().reset()
        self.__first_prompt = True
