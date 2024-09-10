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

class ThoughtEnactor(BaseLLMEnactor):

    def __init__(self, *, recorder:str, model:str = None, name:str = "Thought Enactor", provider:str = None, temperature=0, **kwargs):
        super().__init__(recorder=recorder, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Thought Enactor {name} created")
    
    def enact(self, thought, *, narrative):
        '''
        Enacts the thought.
        '''        
        # For an extended expression, the system prompt is already executed in one of the previous expressions.
        thought.narrative = narrative
        thought.store = narrative.store
        thought.fixture.before()

        if thought.has_directive():
            narrative.append_directive(thought.directive)
        
        log_debug(f"Executing Thought with {len(thought)} expression(s).")
        self.recorder.record_begin_thought(thought)
        
        from swayam.llm.enact.expression import ExpressionEnactor
        from swayam.llm.phase.expression.expression import UserExpression
        expression_enactor = ExpressionEnactor(recorder=self.recorder, model=self.model, provider=self.provider, temperature=self.temperature)
        
        for expressions in thought:
            if isinstance(expressions, UserExpression):
                expressions = [expressions]
            else:
                expressions.store = thought.store
                expressions = expressions() # Lazy loading
            for expression in expressions:
                expression.story = thought.story
                expression.thought = thought.purpose
                thought.node_fixture.before()
                expression_enactor.enact(expression, narrative=narrative)
                thought.node_fixture.after()
            
        thought.fixture.after()