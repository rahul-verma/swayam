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

from typing import List

from pydantic import BaseModel, Field
from swayam import Template

class DirInfoModel(BaseModel):
    dir_name:str = Field(..., description="Name of the directory", examples=["tools"])
    dir_path:str = Field(..., description="Full or Project Relative Path of the directory", examples=["/project/home/user", "user/test"])
    
class DirsInfoModel(BaseModel):
    files: List[DirInfoModel] = Field(..., description="List of FileInfoModel objects")
    
DirInfo = Template.build("DirInfo", model=DirInfoModel) 
DirsInfo = Template.build("DirsInfo", model=DirsInfoModel)