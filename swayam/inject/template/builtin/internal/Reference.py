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

from typing import List, Union

from pydantic import BaseModel, Field
from swayam import Template

class ReferenceModel(BaseModel):
    reference_description :str = Field(..., description="Description of the reference")
    reference_template:str = Field(..., description="Template of an entry in its contents")
    reference_content:str = Field(..., description="All contents or content of one entry, depending on the iterator logic.")
    reference_writeup: str = Field("", description="Writeup of the reference in singular or plural form.")

Reference = Template.build("Reference", model=ReferenceModel)