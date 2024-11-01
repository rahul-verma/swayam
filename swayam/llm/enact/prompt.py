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

from swayam.llm.phase.prompt.prompt import UserPrompt
from swayam.llm.phase.prompt.response import LLMResponse
from .base import BaseLLMEnactor
from swayam import Template

class PromptEnactor(BaseLLMEnactor):

    def __init__(self, *, recorder:str, model:str = None, name:str = "Expression Enactor", provider:str = None, temperature=0, **kwargs):
        super().__init__(recorder=recorder, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Expression Enactor {name} created")
    
    def enact(self, prompt, *, narrative, report=True):
        '''
        Runs the expression and returns the result.
        '''        
        # For an extended expression, the system prompt is already executed in one of the previous expressions.
        
        #conversation = expression.narrative.conversation
                
        prompt.vault = narrative.vault
        
        prompt.frame.prologue()

        log_debug("Processing prompt...")
        prompt.process_for_report()
        
        conversation = narrative.conversation
        
        # Appending happens via the Narrator Narrative so that dynamic variables can be considered.
        conversation.append_prompt(prompt)
        if report:
            self.recorder.record_prompt(prompt, conversation)
        log_debug("Finished processing prompt...")

        log_debug("Executing prompt...")
        from swayam.llm.interpret import Model
        self.__client = Model.create_client(config=prompt.model, prompt_config=self.prompt_config)
        llm_response = self.__client.execute_messages(messages=conversation.messages, out_template=prompt.out_template, actions=prompt.actions)
        log_debug("Handling Response.")
        
        conversation.append_assistant_response(llm_response.as_dict())
        
        if report:
            self.recorder.record_response(prompt, llm_response)
        log_debug("Updated Narrative with Response message.")
        
        if llm_response.error:
            print(llm_response.content)
            raise ValueError("There was an error in the LLM request. The response was returned as None.")
        
        narrative.vault.set("response_content", llm_response.as_dict()["content"], phase=prompt)
        
        action_results = {}
        drafter_found = False
        if llm_response.message.tool_calls:
            response_messages = []
            
            for tool in llm_response.message.tool_calls:
                if tool.function.name == "Draft":
                    drafter_found = True
                action_results[tool.id] = {"name": tool.function.name, "arguments": tool.function.arguments}
                if json.loads(tool.function.arguments) is not None:
                    action_response = prompt.call_action(tool.id, tool.function.name, **json.loads(tool.function.arguments))
                    action_results[tool.id]["response"] = json.dumps(action_response.content)
                else:
                    action_results[tool.id]["response"] = "null"
                self.recorder.record_action_response(action_response)
                response_messages.append(action_response)
                conversation.append_action_response(action_response)
            narrative.vault.set("action_results",  action_results, phase=prompt)
        else:
            if prompt.draft_mode:
                prompt.call_action("internal42", "Draft", content=llm_response.content)
            response_messages = llm_response.message
            
        prompt.frame.epilogue()

        