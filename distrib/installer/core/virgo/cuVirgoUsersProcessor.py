# installer - virgo users
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
import getpass
import json
import os
from tools.AConfParamNotNone import AConfParamNotNone
from tools.AConfUnit import AConfUnit

__author__ = 'mffrench'


class cpVirgoAdminUserName(AConfParamNotNone):

    name = "##adminusername"
    description = "Virgo admin user name"
    hide = False

    def __init__(self):
        self.value = None


class cpVirgoAdminUserPassword(AConfParamNotNone):

    name = "##adminuserpassword"
    description = "Virgo admin user password"
    hide = True

    def __init__(self):
        self.value = None


class cuVirgoUsersProcessor(AConfUnit):

    def __init__(self, targetConfDir):
        self.confUnitName = "Virgo Users"
        self.confTemplatePath = os.path.abspath("resources/templates/virgo/org.eclipse.virgo.kernel.users.properties.tpl")
        self.confFinalPath = targetConfDir + "org.eclipse.virgo.kernel.users.properties"
        userName = cpVirgoAdminUserName()
        userPassword = cpVirgoAdminUserPassword()
        self.paramsDictionary = {
            userName.name: userName,
            userPassword.name: userPassword
        }

class virgoUsersSyringe:

    def __init__(self, targetConfDif, silent):
        self.silent = silent
        self.virgoUsersCUProcessor = cuVirgoUsersProcessor(targetConfDif)
        virgoUsersCUJSON = open("resources/configvalues/virgo/cuVirgoUsers.json")
        self.virgoUsersCUValues = json.load(virgoUsersCUJSON)
        virgoUsersCUJSON.close()

    def getUsersConf(self):
        return {
            'username':self.virgoUsersCUValues[cpVirgoAdminUserName.name],
            'password':self.virgoUsersCUValues[cpVirgoAdminUserPassword.name]
        }

    def shootBuilder(self):
        if not self.silent:
            virgoAdminUserNameIsDefined = False
            virgoAdminUserNameDefault = self.virgoUsersCUValues[cpVirgoAdminUserName.name]
            virgoAdminUserNameDefaultUI = "[default - " + virgoAdminUserNameDefault + "] "
            while not virgoAdminUserNameIsDefined:
                username = input("%-- >> Define Virgo admin user name " + virgoAdminUserNameDefaultUI + ": ")
                if username != "" and username is not None:
                    self.virgoUsersCUValues[cpVirgoAdminUserName.name] = username
                virgoAdminUserNameIsDefined = True

        self.virgoUsersCUProcessor.setKeyParamValue(cpVirgoAdminUserName.name, self.virgoUsersCUValues[cpVirgoAdminUserName.name])

        if not self.silent:
            virgoAdminUserPasswordIsDefined = False
            virgoAdminUserPasswordDefault = self.virgoUsersCUValues[cpVirgoAdminUserPassword.name]

            while not virgoAdminUserPasswordIsDefined:
                password = getpass.getpass("%-- >> Define Virgo admin password : ")
                if password != "" and password is not None:
                    self.virgoUsersCUValues[cpVirgoAdminUserPassword.name] = password
                virgoAdminUserPasswordIsDefined = True

        self.virgoUsersCUProcessor.setKeyParamValue(cpVirgoAdminUserPassword.name, self.virgoUsersCUValues[cpVirgoAdminUserPassword.name])

    def inject(self):
        virgoUsersCUJSON = open("resources/configvalues/virgo/cuVirgoUsers.json","w")
        jsonStr = json.dumps(self.virgoUsersCUValues, sort_keys=True, indent=4, separators=(',', ': '))
        virgoUsersCUJSON.write(jsonStr)
        virgoUsersCUJSON.close()
        self.virgoUsersCUProcessor.process()