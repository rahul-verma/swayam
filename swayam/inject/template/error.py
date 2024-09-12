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

from swayam.inject.error import *

class TemplateValidationError(InjectableObjectError):
    
    def __init__(self, template, *, provided_input, error):
        super().__init__(template, error=f"Invalid input data for creating structure. Expected: {template.definition}. Provided input: {provided_input}. Error: {error}")
        
class DataAttributeDoesNotExistError(InjectableObjectError):
    
    def __init__(self, data, *, attribute):
        super().__init__(data.template, error=f"Attribute {attribute} does not exist in template {data.as_dict()}.")