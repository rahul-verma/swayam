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

from .FrameInjectable import InjectableModel
    
class DrafterDefinitionModel(BaseModel):
    definitions: List[str] = Field(..., title="Children Definition names", description="Children Definition names to be repeated.")
    artifact: str = Field(..., title="Artifact name", description="Name of the artifact to draft")
    
class DrafterModel(BaseModel):
    draft: DrafterDefinitionModel = Field(..., title="Draft Definition", description="Draft dictionary.")