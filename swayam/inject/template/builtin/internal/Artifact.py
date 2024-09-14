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

class ReferenceDependencyModel(BaseModel):
    name: str = Field(..., description="Name of the reference.")
    iter_content: bool = Field(False, description="Whether to iterate over the contents of the reference.")

class ArtifactModel(BaseModel):
    singular_name: str = Field(None, description="Singular name for each entry in contents.")
    plural_name: str = Field(None, description="Plural name for all entries in contents. If not provided, it is taken from singular name by suffixing 's'.")
    description: str = Field(None, description="Description of an entry in its content. If not provided, it is taken from Template description.")
    template: str = Field(None, description="Name of the Swayam Template for each unit in contents. Default is TextContent.")
    refer: List[Union[str, ReferenceDependencyModel]] = Field(list(), description="List of references that this draft depends on.")
    feed: List[Union[str,InjectableModel]] = Field(list(), description="List of references that this draft depends on.")
    interim: bool = Field(False, description="Whether this draft is an interim draft. In such a case, it is not stored as a reference.")
    store_as: str = Field(None, description="Name of the reference to store this draft. If not provided, it is stored as the name of the draft. A prefix 'generated_' is added to the name of the reference in both the cases.")
    
Artifact = Template.build("Artifact", model=ArtifactModel)