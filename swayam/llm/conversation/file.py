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
import importlib
from abc import ABC, abstractmethod

class ConversationFile:
    
    def __init__(self, *, role, file_name):
        self.__role = role
        self.__file_name = file_name
        
    @property
    def role(self):
        return self.__role
    @property
    def file_name(self):
        return self.__file_name

class ConversationFileLoader:
    
    def __init__(self):
        pass
        
    def __getattr__(self, name):
        return ConversationFile(file_name=name)
        
        