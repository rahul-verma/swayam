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

import inspect

def get_caller_module_file_location():

    # Get the current stack
    stack = inspect.stack()

    # Function 0: This function
    # Function 1: Inquirer
    # Function 2: Caller
    caller_frames = stack[2:]
    if len(caller_frames) > 3:
        caller_frames = caller_frames[:3]

    # Get the filename of the caller's module
    return str([caller_frame.filename for caller_frame in caller_frames])