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
    
    def enact(self, expression, *, narrative):
        '''
        Runs the expression and returns the result.
        '''
        expression.narrative = narrative
        expression.vault = narrative.vault
        
        expression.frame.prologue()
        from swayam.llm.phase.expression.conversation import Conversation
        conversation = Conversation()
        narrative_instructions = narrative.get_instructions()
        narrative_context_prompt = narrative.get_context_prompt(expression=expression)
        
        log_debug(f"Executing Expression with {len(expression)} prompt(s).")
        self.recorder.record_begin_expression(expression)
        conversation.append_system_prompt(narrative_instructions)
        conversation.append_context_prompt(narrative_context_prompt)

        # prompt_enactor.enact(UserPrompt(text=context_prompt, purpose="Context Setting"), narrative=narrative, report=False)
        
        directive = narrative.get_directive(expression=expression)
        if directive:
            self.recorder.record_directive(directive)
            
        log_debug("Finished processing system prompt.")
        
        from swayam.llm.enact.prompt import PromptEnactor
        prompt_enactor = PromptEnactor(recorder=self.recorder, model=self.model, provider=self.provider, temperature=self.temperature)
        from swayam.llm.phase.prompt.prompt import UserPrompt
        
        for prompts in expression:
            if isinstance(prompts, UserPrompt):
                prompts = [prompts]
            else:
                prompts = prompts() # Lazy loading
            for prompt in prompts:
                log_debug("Processing prompt...")
                # For dynamic variables in Narrative
                prompt.vault = narrative.vault
                prompt.drafter = expression.drafter
                prompt.dynamic_format()
                expression.prompt_frame.prologue()
                if prompt.is_standalone:
                    only_context_conversation = Conversation()
                    only_context_conversation.append_system_prompt(narrative_instructions)
                    only_context_conversation.append_context_prompt(narrative_context_prompt)
                    narrative.conversation = only_context_conversation
                else:
                    narrative.conversation = conversation
                self.recorder.record_conversation(conversation)
                prompt_enactor.enact(prompt, narrative=narrative)
                expression.prompt_frame.epilogue()
            
        expression.frame.epilogue()