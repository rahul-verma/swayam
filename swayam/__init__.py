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
import sys
import warnings
warnings.filterwarnings("ignore")

def __join_paths(*paths):
    return os.path.abspath(os.path.join(*paths))

__root_dir = __join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
sys.path.insert(0, __root_dir)

from swayam.core.facade import Swayam
from swayam.llm.phase.prompt import Prompt
from swayam.llm.phase.expression import Expression
from swayam.llm.phase.thought import Thought
from swayam.llm.phase.story import Story
from swayam.inject.template import Template
from swayam.inject.action import Action
from swayam.inject.driver import Driver
from swayam.inject.cue import Cue
from swayam.inject.snippet import Snippet
from swayam.inject.prop import Prop
from swayam.inject.artifact import Artifact
from swayam.inject.reference import Reference