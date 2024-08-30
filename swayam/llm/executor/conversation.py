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

from swayam.llm.request.types import SystemRequest
from swayam.llm.request.response import LLMResponse
from .base import BaseLLMExecutor

class ActionExecutor(BaseLLMExecutor):

    def __init__(self, *, listener:str, model:str = None, name:str = "Action Executor", provider:str = None, temperature=0, system_request: Union[str,SystemRequest]=None, **kwargs):
        super().__init__(listener=listener, name=name, provider=provider, model=model, temperature=temperature, **kwargs)            
        log_debug(f"Action Executor {name} created")

    def load(self):
        from swayam.llm.model import Model
        self.__client = Model.create_client(config=self.model_config, request_config=self.request_config)
    
    def execute(self, action):
        '''
        Runs the action and returns the result.
        '''        
        # For an extended action, the system request is already executed in one of the previous actions.
        
        action_context = action.context.action_context
        
        log_debug(f"Executing Action with {len(action)} request(s).")
        if not action.extends_previous_action:
            self.listener.report_begin_action(action)
            if action.is_new():
                if action.has_system_request():
                    # For dynamic variables in Agent store
                    action.context.format_request(action.system_request)
                    action.system_request.process_for_report()
                    self.listener.report_system_request(action.system_request)
                    
                    action_context.append_request(action.system_request)
                    self.listener.report_context(action_context)
        log_debug("Finished processing system request.")
        
        for request in action:
            log_debug("Processing request...")
            # For dynamic variables in Agent store
            action.context.format_request(request)
            request.process_for_report()
            
            self.listener.report_context(action_context)
            
            # Appending happens via the Agent Context so that dynamic variables can be considered.
            action_context.append_request(request)
            self.listener.report_context(action_context)
            
            self.listener.report_request(request)
            log_debug("Finished processing request...")

            log_debug("Executing request...")
            response = self.__client.execute_messages(messages=action_context.messages, output_structure=request.output_structure, tools=request.tools)
            log_debug("Handling Response.")
            output_message = response.choices[0].message
            llm_response = LLMResponse(output_message)
            
            action_context.append_assistant_response(llm_response.as_dict())
            self.listener.report_context(action_context)
            
            self.listener.report_response(request, llm_response)

            
            log_debug("Updated Context with Response message.")

            if output_message.tool_calls:
                response_messages = []
                for tool in output_message.tool_calls:
                    tool_response = request.call_tool(tool.id, tool.function.name, **json.loads(tool.function.arguments))
                    self.listener.report_tool_response(tool_response)
                    response_messages.append(tool_response)
                    action_context.append_tool_response(tool_response)
                    self.listener.report_context(action_context)
            else: 
                response_messages = output_message
                
        if action.should_store_response:
            stored_message = response_messages
            if type(response_messages) is list:
                stored_message = response_messages[-1]
            from swayam.inject.tool.response import ToolResponse
            if isinstance(stored_message, ToolResponse):
                stored_message = stored_message.content
            else:
                stored_message = stored_message.to_dict()
            if "content" in stored_message and stored_message["content"]:
                action.context.store[action.response_storage_name] = stored_message["content"]

        log_debug(f"Finished Action") 
        return response_messages