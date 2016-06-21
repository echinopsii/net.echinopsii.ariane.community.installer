# installer virgo processor
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
from core.virgo.CUVirgoKernelRegionOSGIConsoleProcessor import VirgoKernelRegionOSGIConsoleSyringe
from core.virgo.CUVirgoUserRegionOSGIConsoleProcessor import VirgoUserRegionOSGIConsoleSyringe
from core.virgo.CUVirgoUsersProcessor import VirgoUsersSyringe
from core.virgo.CUContextDefaultProcessor import ContextDefaultSyringe

__author__ = 'mffrench'


class VirgoProcessor:

    def __init__(self, home_dir_path, silent):
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Virgo configuration : \n")
        self.silent = silent

        self.homeDirPath = home_dir_path
        self.configurationPath = home_dir_path + "/configuration/"
        self.contextPath = self.configurationPath + "/Catalina/localhost"
        self.extrepo = home_dir_path + "/repository/ext/"

        self.virgoUsersSyringe = VirgoUsersSyringe(self.configurationPath, self.silent)
        self.virgoUsersSyringe.shoot_builder()

        self.virgoKernelRegionOSGIConsoleSyringe = VirgoKernelRegionOSGIConsoleSyringe(self.configurationPath,
                                                                                       self.silent)
        self.virgoKernelRegionOSGIConsoleSyringe.shoot_builder()

        self.virgoUserRegionOSGIConsoleSyringe = VirgoUserRegionOSGIConsoleSyringe(self.extrepo, self.silent)
        self.virgoUserRegionOSGIConsoleSyringe.shoot_builder()

        self.contextDefaultSyringe = ContextDefaultSyringe(self.contextPath, self.homeDirPath)

    def process(self):
        self.contextDefaultSyringe.inject()
        self.virgoUsersSyringe.inject()
        self.virgoKernelRegionOSGIConsoleSyringe.inject()
        self.virgoUserRegionOSGIConsoleSyringe.inject()
        return self

    def get_user_region_ssh_params(self):
        username = self.virgoUsersSyringe.get_users_conf().get('username')
        password = self.virgoUsersSyringe.get_users_conf().get('password')
        hostname = self.virgoUserRegionOSGIConsoleSyringe.get_user_region_ssh_params().get('hostname')
        port = self.virgoUserRegionOSGIConsoleSyringe.get_user_region_ssh_params().get('port')
        return {
            'username': username,
            'password': password,
            'hostname': hostname,
            'port': port
        }
