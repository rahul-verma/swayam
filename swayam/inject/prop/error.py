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


class PropInvalidCallableError(InjectableCallError):

    def __init__(self, injectable):
            super().__init__(injectable, 
                             error=f"{injectable.callable.__name__} of type {type(injectable.callable)} was expected to be a generator object which can be called twice, once for setup and once for teardown. Both times it should return a **Template.Result** object. An easy way to do this is by creating a function that has two yield statements.")
            
class PropSetUpError(InjectableCallError):

    def __init__(self, injectable, *, error):
            super().__init__(injectable, 
                             error=f"{injectable.callable.__name__} has an error in setup call (first call). Error: {error}")
            
class PropTearDownError(InjectableCallError):

    def __init__(self, injectable, *, error):
            super().__init__(injectable, 
                             error=f"{injectable.callable.__name__} has an error in teardown call (second call). Error: {error}")