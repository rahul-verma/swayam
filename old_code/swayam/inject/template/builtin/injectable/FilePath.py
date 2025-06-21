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

class FilePathModel(BaseModel):
    file_path:str = Field(..., description="Full or Project Relative Path of the file. Must include file name.", examples=["/home/user/file.txt", "user/file.txt"]) 
    
class FilePathsModel(BaseModel):
    file_paths:List[str] = Field(..., description="Full or Project Relative Path of files. Must include file names.", examples=[["/home/user/file.txt", "user/file.txt"]]) 
    
FilePath = Template.build("FilePath", model=FilePathModel)
FilePaths  = Template.build("FilePaths", model=FilePathModel)