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

import os

from tarkash import FlatFile, IniFile
from tarkash.type.descriptor import *
from tarkash import log_debug
from swayam.type.constant import SwayamOption

class PromptTextFile(FlatFile):
    _path = String(immutable=True)
    
    """
    Loads prompt text from a prompt text file. The file / relative file path must exist, relative to <PROJECT_ROOT_DIR>/prompts
    
    Args:
        file_path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, **kwargs):
        """
        Initializes the FlatFileReader with the provided file path and try_relative_path flag.
        """
        from tarkash import Tarkash
        path = os.path.join(Tarkash.get_option_value(SwayamOption.PROMPTS_ROOT_DIR), path)
        super().__init__(path, **kwargs)
        
        
class PromptIniFile(IniFile):
    _path = String(immutable=True)
    
    """
    Loads prompt text from a prompt text file. The file / relative file path must exist, relative to <PROJECT_ROOT_DIR>/prompts
    
    Args:
        file_path (str): Path to the file. If try_relative_path is True, it is relative to the current working directory.
        
    Keyword Arguments:
        try_relative_path (bool): If True, file_path is relative to the file where the call is made. Else, it is an absolute path.
        
    Raises:
        IncorrectFilePathError: If the file does not exist.
        FileIOError: If there is an error reading the file.
    """
 
    def __init__(self, path, **kwargs):
        """
        Initializes the FlatFileReader with the provided file path and try_relative_path flag.
        """
        from tarkash import Tarkash
        path = os.path.join(Tarkash.get_option_value(SwayamOption.PROMPT_ROOT_DIR), path)
        super().__init__(path, **kwargs)