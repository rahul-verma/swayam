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
from .Injectable import InjectableModel

class EntityModel(BaseModel):
    singular_name: str = Field(None, description="Singular name for the entity.")
    plural_name: str = Field(None, description="Plural name for the aggregates of this entity. If not provided, it is taken from singular name by suffixing 's'.")
    description: str = Field(..., description="Description of the entity. If not provided, it is taken from Template description.")
    template: str = Field(..., description="Name of the Swayam Template for entity content. Default is TextContent.")
    
Entity = Template.build("Entity", model=EntityModel)