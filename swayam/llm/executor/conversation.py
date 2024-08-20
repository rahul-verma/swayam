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

from swayam.llm.prompt.types import SystemPrompt
from swayam.llm.prompt.response import LLMResponse
from .base import BaseLLMExecutor

class ConversationExecutor(BaseLLMExecutor):

    def __init__(self, *, listener:str, model:str = None, name:str = "Conversation Executor", provider:str = None, temperature=0, system_prompt: Union[str,SystemPrompt]=None, **kwargs):
        super().__init__(listener=listener, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Conversation Executor {name} created")

    def load(self):
        from swayam.llm.model import Model
        self.__client = Model.create_client(config=self.model_config, prompt_config=self.prompt_config)
    
    def execute(self, conversation):
        '''
        Runs the conversation and returns the result.
        '''        
        # For an extended conversation, the system prompt is already executed in one of the previous conversations.
        
        print(f"Executing Conversation with {len(conversation)} prompt(s).")
        self.listener.report_begin_conversation(conversation)
        if conversation.has_system_prompt():
            conversation.system_prompt.process_for_report()
            self.listener.report_system_prompt(conversation.system_prompt)
            
            conversation.context.append_prompt(conversation.system_prompt)
            self.listener.report_context(conversation.context)
        log_debug("Finished processing system prompt.")
        
        for prompt in conversation:
            log_debug("Processing prompt...")
            prompt.process_for_report()
            
            self.listener.report_context(conversation.context)
            
            conversation.context.append_prompt(prompt)
            self.listener.report_context(conversation.context)
            
            self.listener.report_prompt(prompt)
            log_debug("Finished processing prompt...")

            log_debug("Executing prompt...")
            response = self.__client.execute_messages(messages=conversation.context.messages, output_structure=prompt.output_structure, tools=prompt.tools)
            log_debug("Handling Response.")
            output_message = response.choices[0].message
            llm_response = LLMResponse(output_message)
            
            conversation.context.append_assistant_response(llm_response.as_dict())
            self.listener.report_context(conversation.context)
            
            self.listener.report_response(prompt, llm_response)

            
            log_debug("Updated Context with Response message.")

            if output_message.tool_calls:
                response_messages = []
                for tool in output_message.tool_calls:
                    tool_response = prompt.call_tool(tool.id, tool.function.name, **json.loads(tool.function.arguments))
                    self.listener.report_tool_response(tool_response)
                    response_messages.append(tool_response)
                    conversation.context.append_tool_response(tool_response)
                    self.listener.report_context(conversation.context)
            else: 
                response_messages = output_message

        log_debug(f"Finished Conversation") 
        return response_messages