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

class LLMResponse:
    
    def __init__(self, message, **kwargs) -> None:
        self.__message = message
        
    @property
    def message(self):
        return self.__message
    
    def as_dict(self) -> dict:
        return self.__message.to_dict()
    
    @classmethod
    def create_response_object(cls, message:dict, **kwargs):
        """
        Creates a response object from the message.
        
        Args:
            message (dict): The message to create the response from.
        """
        return ContentResponse(message, **kwargs)

class ContentResponse(LLMResponse):
    
    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
        self.__content = message.content
        
    @property
    def content(self):
        return self.__content

class FunctionResponse:
    pass

class ToolResponse:
    pass
