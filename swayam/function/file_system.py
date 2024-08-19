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

import os

def list_files(path:str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory '{path}' does not exist.")
    if not os.path.isdir(path):
        raise FileNotFoundError(f"'{path}' is not a directory.")
    file_paths = []
    
    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            # Construct absolute file path
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    
    return file_paths