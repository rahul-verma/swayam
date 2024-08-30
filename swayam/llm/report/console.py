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
import os

from pprint import pprint

from swayam.llm.request import Request
from swayam.llm.action.context import ActionContext
from swayam.llm.request.response import LLMResponse
from swayam.llm.report import Reporter
    
class ConsoleReporter(Reporter):
    def __init__(self):
        super().__init__()
        
    @property
    def enabled(self):
        return self.__enabled
    

    def report_begin_action(self, action) -> None:
        """
        Broadcasts the system request details.
        
        Args:
            request (Request): The request to report.
        """
        pass
    
    def report_system_request(self, request:Request) -> None:
        """
        Reports the request details.
        
        Args:
            request (Request): The request to report.
        """
        self.report_request(request)

    def report_request(self, request:Request) -> None:
        """
        Reports the request details.
        
        Args:
            request (Request): The request to report.
        """
        print("-" * 80)
        print("Request:", f"(Role: {request.role})")
        
        ## Should not print image
        content = request.content
        if type(content) == list:
            print(request.reportable_text)
            print("=" * 100)
            for item in request.reportable_content:
                if item["type"] == "image_url":
                    print(item["local_path"])
        else:
            print(request.content)
        print("-" * 80)

    def report_context(self, context:ActionContext) -> None:
        """
        Reports the context details.

        Args:
            context (ActionContext): Context object with all input messages.
        """
        pass
        
    def report_response(self, request, response:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            response (LLMResponse): Response message from LLM.
        """
        print("Response:")
        print(response.content)
        
    def report_tool_response(self, response) -> None:
        """
        Reports the tool response.

        Args:
            message (dict): ToolResponse object
        """
        pass
        
    def finish(self) -> None:
        """
        Finishes report creation.
        """
        print("-"* 80) 
