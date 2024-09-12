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

import os
import re

def list_files(*, invoker, dir_path:str, file_filter_pattern:str=None):
    from tarkash import Directory
    directory = Directory(dir_path, should_exist=True)
    files_info_list = []
    
    # Walk through the directory tree
    files_info_list = []
    for dirpath, _, filenames in os.walk(directory.full_path):
        for filename in filenames:
            # Construct absolute file path
            if file_filter_pattern is not None and not re.match(file_filter_pattern, filename):
                continue
            file_path = os.path.join(dirpath, filename)
            files_info_list.append(Template.FileInfo(file_name=filename, file_path=file_path).as_dict())
    
    return Template.FilesInfo(files=files_info_list)

DirEnumerator = Action.build("DirEnumerator", 
                         callable=list_files, 
                         description="Recursively lists the full path of files in the provided directory path.",
                         in_template=Template.DirPathFilter,
                         out_template=Template.FilesInfo,
)