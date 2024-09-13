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

from typing import Union, List
from pydantic import BaseModel, Field

from swayam import Template
from .Frame import FrameModel

class DraftModel(BaseModel):
    description: str = Field(..., description="Description of the contents in this draft.")
    template: Union[str, None] = Field(None, description="Name of the Swayam Template for each unit in contents.")
    depends_on: Union[List[str], None] = Field(None, description="List of other drafts that this draft depends on.")
    
Draft = Template.build("Draft", model=DraftModel)