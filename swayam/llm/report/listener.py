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

from swayam.llm.request import Request
from swayam.llm.request.types import SystemRequest
from swayam.llm.action.context import ActionContext

class AgentListener:
    
    def __init__(self, report_config):
        self.__reporters = []
        
        from .console import ConsoleReporter
        from .html import HtmlReporter
        if report_config.display:
            self.__reporters.append(ConsoleReporter())
            
        if report_config.report_html:
            self.__reporters.append(HtmlReporter(config=report_config))
            
    def report_begin_action(self, action) -> None:
        """
        Broadcasts the system request details.
        
        Args:
            request (Request): The request to report.
        """
        for reporter in self.__reporters:
            reporter.report_begin_action(action)
            
    def report_system_request(self, request:SystemRequest) -> None:
        """
        Broadcasts the system request details.
        
        Args:
            request (Request): The request to report.
        """
        for reporter in self.__reporters:
            reporter.report_system_request(request)

    def report_request(self, request:Request) -> None:
        """
        Broadcasts the request details.
        
        Args:
            request (Request): The request to report.
        """
        for reporter in self.__reporters:
            reporter.report_request(request)
    
    def report_context(self, context:ActionContext) -> None:
        """
        Broadcasts the context details.

        Args:
            context (ActionContext): Context object with all input messages.
        """
        for reporter in self.__reporters:
            reporter.report_context(context)
 
    def report_response(self, request, message:dict) -> None:
        """
        Broadcasts the output message.

        Args:
            message (dict): Response dict from LLM.
        """
        for reporter in self.__reporters:
            reporter.report_response(request, message)
            
    def report_tool_response(self, response) -> None:
        """
        Broadcasts the tool response.

        Args:
            message (dict): ToolResponse object
        """
        for reporter in self.__reporters:
            reporter.report_tool_response(response)
            
    def finish(self) -> None:
        """
        Broadcasts finish signal.
        """
        for reporter in self.__reporters:
            reporter.finish()