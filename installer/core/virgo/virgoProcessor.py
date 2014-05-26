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
from core.virgo.cuVirgoKernelRegionOSGIConsoleProcessor import virgoKernelRegionOSGIConsoleSyringe
from core.virgo.cuVirgoUserRegionOSGIConsoleProcessor import virgoUserRegionOSGIConsoleSyringe
from core.virgo.cuVirgoUsersProcessor import virgoUsersSyringe

__author__ = 'mffrench'


class virgoProcessor:

    def __init__(self, homeDirPath, silent):
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Virgo configuration : \n")
        self.silent = silent

        self.homeDirPath = homeDirPath
        self.configurationPath = homeDirPath + "/configuration/"
        self.extrepo = homeDirPath + "/repository/ext/"

        self.virgoUsersSyringe = virgoUsersSyringe(self.configurationPath, self.silent)
        self.virgoUsersSyringe.shootBuilder()

        self.virgoKernelRegionOSGIConsoleSyringe = virgoKernelRegionOSGIConsoleSyringe(self.configurationPath, self.silent)
        self.virgoKernelRegionOSGIConsoleSyringe.shootBuilder()

        self.virgoUserRegionOSGIConsoleSyringe = virgoUserRegionOSGIConsoleSyringe(self.extrepo, self.silent)
        self.virgoUserRegionOSGIConsoleSyringe.shootBuilder()

    def process(self):
        self.virgoUsersSyringe.inject()
        self.virgoKernelRegionOSGIConsoleSyringe.inject()
        self.virgoUserRegionOSGIConsoleSyringe.inject()
        return self

    def getUserRegionSSHParams(self):
        username = self.virgoUsersSyringe.getUsersConf().get('username')
        password = self.virgoUsersSyringe.getUsersConf().get('password')
        hostname = self.virgoUserRegionOSGIConsoleSyringe.getUserRegionSSHParams().get('hostname')
        port = self.virgoUserRegionOSGIConsoleSyringe.getUserRegionSSHParams().get('port')
        return {
            'username': username,
            'password': password,
            'hostname': hostname,
            'port': port
        }