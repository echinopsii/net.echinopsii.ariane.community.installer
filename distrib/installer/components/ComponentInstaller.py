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
from tools.ComponentHook import ComponentHook

__author__ = 'mffrench'

class ComponentInstaller:
    def __init__(self, home_path):
        self.home_path = home_path

    @staticmethod
    def get_installed_components_hook(virgo_home_path):
        hooks = [None, None, None, None, None]
        for file in os.listdir(virgo_home_path + "/ariane/installer/components"):
            if os.path.isdir(virgo_home_path + "/ariane/installer/components/" + file) and \
                    os.path.exists(virgo_home_path + "/ariane/installer/components/" + file +
                                   "/arianecomponenthook.json"):
                hook = ComponentHook(virgo_home_path + "/ariane/installer/components/" + file +
                                     "/arianecomponenthook.json")
                hooks[hook.order] = hook
        return hooks

class ComponentProcessor:
    def __init__(self, home_path, bus_processor, dist_dep_type, silent):
        self.home_path = home_path
        self.silent = silent
        self.directoryDBConfig = None
        self.idmDBConfig = None
        self.busProcessor = bus_processor
        self.dist_dep_type = dist_dep_type

    def process(self):
        for hook in ComponentInstaller.get_installed_components_hook(self.home_path):
            if hook is not None:
                imported = getattr(__import__(hook.hookPackage + "." + hook.hookModule, fromlist=[hook.hookClass]),
                                   hook.hookClass)
                imported_sgt = imported(self.home_path, self.directoryDBConfig, self.idmDBConfig,
                                        self.busProcessor, self.silent).process()
                self.directoryDBConfig = imported_sgt.directoryDBConfig
                self.idmDBConfig = imported_sgt.idmDBConfig
        return self
