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

class ReportConfig:
    
    def __init__(self, *, display=False, report_html=True, show_in_browser=True):
        self._display = display
        self._report_html = report_html
        self._show_in_browser = show_in_browser

    @property
    def display(self):
        return self._display
    
    @property
    def report_html(self):
        return self._report_html
    
    @property
    def show_in_browser(self):
        return self._show_in_browser
    
    @property
    def run_id(self):
        return self._run_id        
        
    