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
from swayam.function.file_system import *
from swayam.llm.structure.builtin import Path

ListFiles = Tool.build("ListFiles", 
                         target=list_files, 
                         desc="Recursively lists the full path pf files in the provided directory path.",
                         call_structure=Path
)