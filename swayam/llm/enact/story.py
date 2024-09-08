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

import json
from typing import Union

from tarkash import log_debug
from .base import BaseLLMEnactor

class StoryEnactor(BaseLLMEnactor):

    def __init__(self, *, recorder:str, model:str = None, name:str = "Story Enactor", provider:str = None, temperature=0, **kwargs):
        super().__init__(recorder=recorder, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Story Enactor {name} created")
    
    def enact(self, story, *, narrative):
        '''
        Enacts the story.
        '''        
        # For an extended expression, the system prompt is already executed in one of the previous expressions.
        
        if story.has_directive():
            narrative.append_directive(story.directive)
        
        log_debug(f"Executing Story with {len(story)} thought(s).")
        self.recorder.record_begin_story(story)
        
        story.store = narrative.store
        story.fixture.before()
        
        from swayam.llm.enact.thought import ThoughtEnactor
        thought_enactor = ThoughtEnactor(recorder=self.recorder, model=self.model, provider=self.provider, temperature=self.temperature)
        
        for thought in story:
            log_debug("Processing prompt...")
            thought.story = story.purpose
            story.node_fixture.before()
            thought_enactor.enact(thought, narrative=narrative)
            story.node_fixture.after()
            
        story.fixture.after()