# Ariane components installer main
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
import os
from tools.ComponentHook import componentHook

__author__ = 'mffrench'

class componentInstaller:
    def __init__(self, virgo_home_path):
        self.virgo_home_path = virgo_home_path

    @staticmethod
    def get_installed_components_hook(virgo_home_path):
        hooks = [None, None, None, None, None]
        for file in os.listdir(virgo_home_path + "/ariane/installer/components"):
            if os.path.isdir(virgo_home_path + "/ariane/installer/components/" + file) and \
                    os.path.exists(virgo_home_path + "/ariane/installer/components/" + file +
                                   "/arianecomponenthook.json"):
                hook = componentHook(virgo_home_path + "/ariane/installer/components/" + file +
                              "/arianecomponenthook.json")
                hooks[hook.order] = hook
        return hooks

class componentProcessor:
    def __init__(self, virgo_home_path, silent):
        self.virgo_home_path = virgo_home_path
        self.silent = silent
        self.directoryDBConfig = None
        self.idmDBConfig = None

    def process(self):
        for hook in componentInstaller.get_installed_components_hook(self.virgo_home_path):
            if hook is not None:
                imported = getattr(__import__(hook.hookPackage + "." + hook.hookModule, fromlist=[hook.hookClass]),
                                   hook.hookClass)
                imported_sgt = imported(self.virgo_home_path, self.directoryDBConfig, self.idmDBConfig, self.silent).\
                    process()
                self.directoryDBConfig = imported_sgt.directoryDBConfig
                self.idmDBConfig = imported_sgt.idmDBConfig
        return self
