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
from json import JSONDecodeError
from typing import Any
from pydantic import BaseModel, Field, field_serializer

from swayam import Template


class JsonContentModel(BaseModel):
    
    content: Any = Field(..., title="Json Input Content", description="The provided object should be serialisable to Json using json.dump/dumps.")
    
    # @field_serializer()
    # def input_content(cls, v):
    #     return json.dumps(v)
    
    # @input_content.setter
    # def input_content(self, v: str):
    #     # Automatically add the prefix when storing the value
    #     try:
    #         json.dumps(v)
    #     except JSONDecodeError as e:
    #         raise ValueError("Invalid JSON content. Error:", e)

# _prefix = "PREFIX_"

# ## The methods used here are meant to prevent serialization warnings.
# class SerializedJsonModel(BaseModel):
    
#     json_content: str = Field(..., title="Json Text Content", description="Json object serialized into a string using json.dump/dumps.")
    
#     @property
#     def json_content(self) -> str:
#         return self.__dict__['json_content'][len(_prefix):]

#     @json_content.setter
#     def json_content(self, v: str):
#         # Automatically add the prefix when storing the value
#         try:
#             json.loads(v)
#         except JSONDecodeError as e:
#             raise ValueError("Invalid content. Error:", e)
#         else:
#             self.__dict__['json_content'] = f"{_prefix}{v}"
        
# class SerializedJsonListModel(BaseModel):
    
#     json_content_list: List[str] = Field(..., title="List of Serialised Json Contents", description="List of Json contents serialized into a string using json.dump/dumps.")
    
#     @property
#     def json_content_list(self) -> str:
#         return [item[len(_prefix):] for item in self.__dict__['content']]

#     @json_content_list.setter
#     def json_content_list(self, v: str):
#         # Automatically add the prefix when storing the value
#         try:
#             [json.loads(item) for item in v]
#         except JSONDecodeError as e:
#             raise ValueError("Invalid content. Error:", e)
#         else:
#             self.__dict__['json_content_list'] = [f"{_prefix}{item}" for item in v]    
    
# SerializedJson = Template.build("SerializedJson", model=SerializedJsonModel)
# SerializedJsonList= Template.build("SerializedJsonList", model=SerializedJsonListModel)

JsonContent = Template.build("JsonContent", model=JsonContentModel)