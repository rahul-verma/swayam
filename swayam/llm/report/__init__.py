
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

from abc import ABC, abstractmethod
from swayam.llm.request import Request
from swayam.llm.request.types import SystemRequest
from swayam.llm.action.context import ActionContext
from swayam.llm.request.response import LLMResponse

class Reporter(ABC):
    
    def __init__(self, **kwargs):
        pass
    
    @abstractmethod
    def report_begin_action(self, action) -> None:
        """
        Broadcasts the system request details.
        
        Args:
            request (Request): The request to report.
        """
        pass
    
    @abstractmethod
    def report_request(self, request:Request) -> None:
        """
        Reports the request details.
        
        Args:
            request (Request): The request to report.
        """
        pass
        
    @abstractmethod
    def report_context(self, context:ActionContext) -> None:
        """
        Reports the context details.

        Args:
            context (ActionContext): Context object with all input messages.
        """
        pass

        
    def report_response(self, message:LLMResponse) -> None:
        """
        Reports the LLM response.

        Args:
            message (LLMResponse): Response message from LLM.
        """
        pass
    
    @abstractmethod
    def finish(self) -> None:
        """
        Finishes report creation.
        """
        pass