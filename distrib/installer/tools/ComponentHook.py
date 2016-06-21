# Component description tools
#
# Copyright (C) 2014 Mathilde Ffrench
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
import os

__author__ = 'mffrench'


class ComponentHook:

    def __init__(self, component_hook_path):
        if os.path.exists(component_hook_path) and os.path.isfile(component_hook_path):
            json_component_hook = json.load(open(component_hook_path))
            self.order = json_component_hook["order"]
            self.hookPackage = json_component_hook["hook"]["package"]
            self.hookModule = json_component_hook["hook"]["module"]
            self.hookClass = json_component_hook["hook"]["class"]
        else:
            raise FileNotFoundError(os.path.abspath(component_hook_path))