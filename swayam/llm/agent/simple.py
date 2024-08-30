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
from .context import AgentContext

class SimpleAgent:
    
    def __init__(self, display=False, report_html=True, run_id=None):
        self.__context = AgentContext()
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
        
    def __prepare_for_execution(self, *, show_in_browser):
        log_debug(f"Setting show_in_browser to {show_in_browser}.")
        self.__report_config.show_in_browser = show_in_browser
        
        
    def __execute_user_request(self, user_request):
        from swayam import Action
        log_debug(f"Converting UserRequest to Action.")
        action = Action.requests(user_request, reset_context=False)
        action.extends_previous_action = True
        return self.__execute_action(action)
    
    def __execute_action(self, action):
        from swayam.llm.action.context import ActionContext
        from swayam.llm.executor.action import ActionExecutor

        if action.reset_context:
            self.__context.reset_action_context()

        # Set context of action
        if not action.standalone:
            action.context = self.__context
        else:
            # Set empty context
            action.context = AgentContext()
        
        log_debug(f"Executing Action with ActionAgent.")
        agent = ActionExecutor(listener=self.__listener)
        
        # If a the context is non-empty then the system request is already set in it.
        log_debug(f"New context-free action?", action.is_new())
        log_debug(f"Action has an already assigned system request?", action.has_system_request()) 
        if action.is_new() and not action.has_system_request():
            log_debug(f"Setting default system request from the Agent.")
            action.system_request = agent.system_request
            
        log_debug("Validating action.")
        if action.is_new() and not action.has_system_request():
            raise ValueError("It's a new action, but no SystemRequest was found. Review.")
        
        if not action.is_new() and action.has_system_request():
            raise ValueError("As it is continued action, the system request is already set in the context. So, the context found in this action is going to be ignored. Review.")
            
        from swayam.inject.tool.response import ToolResponse
        log_debug(f"Executing Action with ActionAgent.")
        def process_output(in_data):
            if in_data.content:
                return in_data.content
            elif isinstance(in_data, ToolResponse):
                return in_data.content
            elif "tool_calls" in in_data and in_data["tool_calls"]:
                return f'Tool Call {in_data["tool_calls"]["function"]["name"]} suggested.'
                
        output = agent.execute(action)
        
        if type(output) is list:
            if len(output) == 1:
                return process_output(output[0])
            elif len(output) == 0:
                return None
            else:
                return [process_output(o) for o in output]
        else:
            return process_output(output)
        
    def __execute_task(self, task):
        output = None
        for action in task:
            output = self.__execute_action(action)
        return output
    
    def execute(self, executable, show_in_browser=False):
        """
        Executes a part of or complete strategy.
        
        The Agent can execute any of the following types of objects:
        - A User Request object
        - A Action object
        - A Task object: Not supported yet
        - A Strategy object: Not supported yet
        
        Args:
            executable: The object to execute.
            show_in_browser: If True, the HTML report will be displayed in the browser. Default is False.
        """
        
        log_debug(f"Executing Agent executable object of type {type(executable)}.")
        self.__prepare_for_execution(show_in_browser=show_in_browser)
        
        from swayam.llm.request.types import UserRequest
        from swayam.llm.action.action import LLMAction
        from swayam.llm.task.task import LLMTask
        
        if not isinstance(executable, (str, UserRequest, LLMAction, LLMTask)):
            raise TypeError(f"Cannot execute object of type {type(executable)}. It must be an instance of str, UserRequest, LLMAction, LLMTask, or Strategy.")
        
        output = None
        if isinstance(executable, str):
            from swayam.llm.request import Request
            log_debug(f"Converting user request string to LLMAction.")
            output = self.__execute_user_request(Request.text(executable))
        if isinstance(executable, UserRequest):
            log_debug(f"Converting UserRequest to LLMAction.")
            output = self.__execute_user_request(executable)
        elif isinstance(executable, LLMAction):
            output = self.__execute_action(executable)
        elif isinstance(executable, LLMTask):
            output = self.__execute_task(executable)
            
        self.__listener.finish()
        return output