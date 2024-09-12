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

from swayam.inject.driver import Driver
from swayam import Action

import os
from swayam import Driver, Template

def get_file_info(*, invoker, dir_path, file_filter_pattern=None):
    from swayam import Action
    for file_info in Action.DirEnumerator(dir_path=dir_path, file_filter_pattern=file_filter_pattern)["files"]:
        yield Template.FileInfo(**file_info)

DirFileInfo = Driver.build("DirFileInfo", 
                                 callable=get_file_info,
                                 in_template=Template.DirPathFilter, 
                                 out_template=Template.FileInfo)

