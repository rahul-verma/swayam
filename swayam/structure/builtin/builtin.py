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

from typing import Union

from pydantic import BaseModel, Field
from swayam import Structure

file_name_field = Field(..., description="Name of the file", examples=["file.txt"])
file_path_field = Field(..., description="Full or Project Relative Path of the file. Must include file name.", examples=["/home/user/file.txt", "user/file.txt"])

dir_name_field = Field(..., description="Name of the directory", examples=["tools"])
dir_path_field = Field(..., description="Full or Project Relative Path of the directory", examples=["/project/home/user", "user/test"])


class DirPathModel(BaseModel):
    dir_path:str = Field(..., description=dir_name_field.description, examples=dir_name_field.examples)
    file_filter_pattern:Union[str,None] = Field(default=None, description="Regular Expression pattern to filter (include) the files. Default is None.", examples=".*\.txt")
    
class FilePathModel(BaseModel):
    file_path:str = Field(..., description=file_path_field.description, examples=file_path_field.examples)    

class FileInfoModel(BaseModel):
    file_name:str = Field(..., description=file_name_field.description, examples=file_name_field.examples)
    file_path:str = Field(..., description=file_path_field.description, examples=file_path_field.examples)
    
class FileContentModel(BaseModel):
    file_name:str = Field(..., description=file_name_field.description, examples=file_name_field.examples)
    file_path:str = Field(..., description=file_path_field.description, examples=file_path_field.examples)
    file_content: str = Field(..., description="Content of the file")

DirPath = Structure.build("DirPath", model=DirPathModel)
FilePath, FilePathList  = Structure.build("FilePath", model=FilePathModel, return_composite=True)
FileInfo, FileInfoList = Structure.build("FileInfo", model=FileInfoModel, return_composite=True)  
FileContent, FileContentList = Structure.build("FileContent", model=FileContentModel, return_composite=True)