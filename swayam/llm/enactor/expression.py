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

class ExpressionEnactor(BaseLLMEnactor):

    def __init__(self, *, recorder:str, model:str = None, name:str = "Expression Enactor", provider:str = None, temperature=0, **kwargs):
        super().__init__(recorder=recorder, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Expression Enactor {name} created")
        
        self.__default_directive = "You are a helpful assistant. You deliberate over the information I provide and my requests. You provide me with the fact-based answers to the best of your ability. Don't hallucinate."
    
    def enact(self, expression, *, narrative):
        '''
        Runs the expression and returns the result.
        '''        
        # For an extended expression, the system prompt is already executed in one of the previous expressions.
        
        directive = self.__default_directive
        if expression.has_directive():
            directive = expression.directive
        
        log_debug(f"Executing Expression with {len(expression)} prompt(s).")
        self.recorder.record_begin_expression(expression)
        conversation = narrative.conversation
        if len(conversation) == 0:
            # For dynamic variables in Narrator store
            #expression.narrative.format_prompt(directive)
            #expression.directive.process_for_report()
            self.recorder.record_directive(directive)
            
            conversation.append_directive(directive)
            self.recorder.record_conversation(conversation)
        log_debug("Finished processing system prompt.")
        
        from swayam.llm.enactor.prompt import PromptEnactor
        prompt_enactor = PromptEnactor(recorder=self.recorder, model=self.model, provider=self.provider, temperature=self.temperature)
        
        for prompt in expression:
            log_debug("Processing prompt...")
            # For dynamic variables in Narrator store
            narrative.format_prompt(prompt)
            prompt_enactor.enact(prompt, narrative=narrative)