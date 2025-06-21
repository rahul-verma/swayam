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

from swayam import Action, Template
from swayam.inject.template.builtin import *

import os
import re

def read_file(*, invoker, file_path:str):
    from tarkash import FlatFile
    file = FlatFile(file_path)
    return Template.TextFileContent(
        file_name=os.path.basename(file_path), 
        file_path=file.full_path, 
        file_content=file.content)

ReadTextFile = Action.build("ReadTextFile", 
                         callable=read_file, 
                         description="Returns the contents of file (in text mode).",
                         in_template=Template.FilePath,
                         out_template=Template.TextFileContent
)