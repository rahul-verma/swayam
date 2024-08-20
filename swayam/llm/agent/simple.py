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

from datetime import datetime
from tarkash import log_debug

class SimpleAgent:
    
    def __init__(self, display=False, report_html=True, run_id=None):
        from swayam.llm.conversation.context import PromptContext
        self.__context = PromptContext()
        from swayam.llm.config.report import ReportConfig
        self.__report_config = ReportConfig(display=display, report_html=report_html, show_in_browser=False)
        if not run_id:
            self.__report_config._run_id = datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            self.__report_config._run_id = str(run_id)
            
        from swayam.llm.report.listener import AgentListener
        log_debug(f"Creating Listener")
        self.__listener = AgentListener(self.__report_config)
        log_debug("Agent initialized.")
        
    def __prepare_for_execution(self, *, reset_context, show_in_browser):
        if reset_context:
            log_debug("Resetting context...")
            self.__context.reset()

        log_debug(f"Setting show_in_browser to {show_in_browser}.")
        self.__report_config.show_in_browser = show_in_browser
        
        
    def __execute_user_prompt(self, user_prompt):
        from swayam import Conversation
        log_debug(f"Converting UserPrompt to Conversation.")
        conversation = Conversation.prompts(user_prompt)
        return self.__execute_conversation(conversation)
    
    def __execute_conversation(self, conversation):
        from swayam.llm.executor.conversation import ConversationExecutor
        # Set context of conversation
        conversation.context = self.__context
        
        log_debug(f"Executing Conversation with ConversationAgent.")
        agent = ConversationExecutor(listener=self.__listener)
        
        # If a the context is non-empty then the system prompt is already set in it.
        log_debug(f"New context-free conversation?", conversation.is_new())
        log_debug(f"Conversation has an already assigned system prompt?", conversation.has_system_prompt()) 
        if conversation.is_new() and not conversation.has_system_prompt():
            log_debug(f"Setting default system prompt from the Agent.")
            conversation.system_prompt = agent.system_prompt
            
        log_debug("Validating conversation.")
        if conversation.is_new() and not conversation.has_system_prompt():
            raise ValueError("It's a new conversation, but no SystemPrompt was found. Review.")
        
        if not conversation.is_new() and conversation.has_system_prompt():
            raise ValueError("As it is continued conversation, the system prompt is already set in the context. So, the context found in this conversation is going to be ignored. Review.")
            
        from swayam.llm.tool.response import ToolResponse
        log_debug(f"Executing Conversation with ConversationAgent.")
        def process_output(in_data):
            if in_data.content:
                return in_data.content
            elif isinstance(in_data, ToolResponse):
                return in_data.content
            elif "tool_calls" in in_data and in_data["tool_calls"]:
                return f'Tool Call {in_data["tool_calls"]["function"]["name"]} suggested.'
                
        output = agent.execute(conversation)
        
        if type(output) is list:
            if len(output) == 1:
                return process_output(output[0])
            elif len(output) == 0:
                return None
            else:
                return [process_output(o) in output]
        else:
            return process_output(output)
                
    
    def execute(self, executable, reset_context=True, show_in_browser=False):
        """
        Executes a part of or complete directive.
        
        The Agent can execute any of the following types of objects:
        - A User Prompt object
        - A Conversation object
        - A Task object: Not supported yet
        - A Directive object: Not supported yet
        
        Args:
            executable: The object to execute.
            reset_context: If True, the context will be reset before executing the object. Default is True.
            show_in_browser: If True, the HTML report will be displayed in the browser. Default is False.
        """
        
        log_debug(f"Executing Agent executable object of type {type(executable)}.")
        self.__prepare_for_execution(reset_context=reset_context, show_in_browser=show_in_browser)
        
        from swayam.llm.prompt.types import UserPrompt
        from swayam.llm.conversation.conversation import LLMConversation
        
        if not isinstance(executable, (UserPrompt, LLMConversation)):
            raise TypeError(f"Cannot execute object of type {type(executable)}. It must be an instance of UserPrompt, LLMConversation, Task, or Directive.")
        
        output = None
        if isinstance(executable, UserPrompt):
            log_debug(f"Converting UserPrompt to LLMConversation.")
            output = self.__execute_user_prompt(executable)
        elif isinstance(executable, LLMConversation):
            output = self.__execute_conversation(executable)
            
        self.__listener.finish()
        return output