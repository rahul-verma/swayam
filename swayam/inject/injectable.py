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

class StructuredInjectable:
    
    def __init__(self, name, *, input_structure, output_structure):
        self.__type = self.__class__.__name__
        self.__name = name
        self.__input_structure = input_structure
        self.__output_structure = output_structure
        
    @property
    def type(self):
        return self.__type
    
    @property
    def name(self):
        return self.__name
    
    @property
    def input_structure(self):
        return self.__input_structure
    
    @property
    def output_structure(self):
        return self.__output_structure
    
    @property
    def allowed_keywords(self):
        from_data_model = list(self.__input_structure.keys)
        from_data_model.insert(0, "caller")
        return from_data_model