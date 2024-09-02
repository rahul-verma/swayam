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
from swayam.llm.thought.thought import UserThought
from swayam.llm.enactor.thought import ThoughtEnactor

from .base import BaseNarrator

class ThoughtNarrator(BaseNarrator):

    def __init__(self, display=False, record_html=True, narration=None):
        super().__init__(display=display, record_html=record_html, narration=narration)
    
    def narrate(self, thought):
        """
        Narrates an Expression to an Expression enactor.
        """
        if not isinstance(thought, UserThought):
            raise TypeError(f"ThoughtnNarrator cannot narrate an expression of type {type(thought)}. It must be an UserExpression object.")
        
        log_debug(f"Executing expression.")
        enactor = ThoughtEnactor(recorder=self.recorder)
        enactor.enact(thought, narrative=self.narrative)