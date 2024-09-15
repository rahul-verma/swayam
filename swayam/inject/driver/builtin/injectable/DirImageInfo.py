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

def get_image_info(*, invoker, dir_path:str):
    from tarkash import Tarkash
    from swayam.core.constant import SwayamOption
    epic_dir = Tarkash.get_option_value(SwayamOption.EPIC_DIR)
    screenshots_dir = os.path.join(epic_dir, "data/screenshots")
    for file_info in Driver.DirFileInfo(dir_path=screenshots_dir, file_filter_pattern=".*png"):
        file_path = file_info["file_path"]
        yield Template.ImageInfo(
            reference_writeup=f"### Image Path of provided image __NL__{file_path}__NL__",
            reference_image_file_path=file_path,
            file_name=file_info["file_name"],
            file_path=file_path
        )
        
DirImageInfo = Driver.build(
    "DirImageInfo",
    callable=get_image_info,
    in_template=Template.DirPath,
    out_template=Template.ImageInfo)