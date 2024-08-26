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

from swayam import Tool, Structure
from swayam.inject.structure.builtin import *

import os
import re

def write_file(*, file_name:str, file_path:str, file_content:str):
    from tarkash import FlatFile
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        file.write(file_content)
    return Structure.StringOutput(output="success")

FileWriter = Tool.build("FileWriter", 
                         target=write_file, 
                         description="Writes the File to the disk with the name provided..",
                         input_structure=Structure.FileContent,
                         output_structure=Structure.StringOutput
)