# This file is a part of Tarkash
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

from swayam.inject.generator import Generator
from swayam import Tool

import os
from swayam import Generator, Structure

def get_file_info(, invoker, dir_path, file_filter_pattern=None):
    from swayam import Tool
    for file_info in Tool.DirEnumerator(dir_path=dir_path, file_filter_pattern=file_filter_pattern)["files"]:
        print(file_info)
        yield Structure.FileInfo(**file_info)

DirFileInfo = Generator.build("DirFileInfo", 
                                 callable=get_file_info,
                                 input_structure=Structure.DirPathFilter, 
                                 output_structure=Structure.FileInfo)

