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

from swayam.llm.prompt.prompt import UserPrompt
from swayam.llm.prompt.response import LLMResponse
from .base import BaseLLMEnactor

class PromptEnactor(BaseLLMEnactor):

    def __init__(self, *, recorder:str, model:str = None, name:str = "Expression Enactor", provider:str = None, temperature=0, **kwargs):
        super().__init__(recorder=recorder, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Expression Enactor {name} created")
        self._load()

    def _load(self):
        from swayam.llm.model import Model
        self.__client = Model.create_client(config=self.model_config, prompt_config=self.prompt_config)
    
    def enact(self, prompt, *, narrative):
        '''
        Runs the expression and returns the result.
        '''        
        # For an extended expression, the system prompt is already executed in one of the previous expressions.
        
        #conversation = expression.narrative.conversation
                
        prompt.store = narrative.store

        log_debug("Processing prompt...")
        prompt.process_for_report()
        
        conversation = narrative.conversation
        
        #self.recorder.record_conversation(conversation)
        
        # Appending happens via the Narrator Narrative so that dynamic variables can be considered.
        conversation.append_prompt(prompt)
        self.recorder.record_conversation(conversation)
        self.recorder.record_prompt(prompt)
        log_debug("Finished processing prompt...")

        log_debug("Executing prompt...")
        llm_response = self.__client.execute_messages(messages=conversation.messages, output_structure=prompt.output_structure, tools=prompt.tools)
        log_debug("Handling Response.")
        
        conversation.append_assistant_response(llm_response.as_dict())
        self.recorder.record_conversation(conversation)
        
        self.recorder.record_response(prompt, llm_response)
        log_debug("Updated Narrative with Response message.")
        
        if llm_response.error:
            raise ValueError("There was an error in the LLM request. The response was returned as None.")
        
        narrative.store.set("response_content", llm_response.as_dict()["content"], phase=prompt)
        
        tooling_results = {}

        if llm_response.message.tool_calls:
            response_messages = []
            for tool in llm_response.message.tool_calls:
                tooling_results["tool.id"] = {"name": tool.function.name, "arguments": tool.function.arguments}
                tool_response = prompt.call_tool(tool.id, tool.function.name, **json.loads(tool.function.arguments))
                tooling_results["tool.id"]["response"] = json.dumps(tool_response.content)
                self.recorder.record_tool_response(tool_response)
                response_messages.append(tool_response)
                conversation.append_tool_response(tool_response)
                self.recorder.record_conversation(conversation)
            narrative.store.set("tool_results",  tooling_results, phase=prompt)
        else:
            response_messages = llm_response.message
            
    # if expression.should_store_response:
    #     stored_message = response_messages
    #     if type(response_messages) is list:
    #         stored_message = response_messages[-1]
    #     from swayam.inject.tool.response import ToolResponse
    #     if isinstance(stored_message, ToolResponse):
    #         stored_message = stored_message.content
    #     else:
    #         stored_message = stored_message.to_dict()
    #     if "content" in stored_message and stored_message["content"]:
    #         expression.narrative.store[expression.response_storage_name] = stored_message["content"]