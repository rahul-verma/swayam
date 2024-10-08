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

class StoryModel(FrameModel):
    thoughts: List[str] = Field(..., description="Thought definition names that are included in this story.")
    purpose: Union[str,None] = Field(None, description="A statement describing the purpose of the story.")
    directive: str = Field(None, description="Directive text for the narrative this story builds. This is the first directive in the narrative.")
    
Story = Template.build("Story", model=StoryModel)