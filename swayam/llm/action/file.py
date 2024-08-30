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

class ActionFile:
    
    def __init__(self, *, file_name):
        self.__file_name = file_name

    @property
    def file_name(self):
        return self.__file_name

class ActionFileLoader:
    
    def __init__(self):
        pass
        
    def __getattr__(self, name):
        return ActionFile(file_name=name)
        
        