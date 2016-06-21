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


class CPVirgoAdminUserName(AConfParamNotNone):

    name = "##adminusername"
    description = "Virgo admin user name"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPVirgoAdminUserName, self).is_valid()


class CPVirgoAdminUserPassword(AConfParamNotNone):

    name = "##adminuserpassword"
    description = "Virgo admin user password"
    hide = True

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPVirgoAdminUserPassword, self).is_valid()


class CUVirgoUsersProcessor(AConfUnit):

    def __init__(self, target_conf_dir):
        self.confUnitName = "Virgo Users"
        self.confTemplatePath = os.path.abspath(
            "resources/templates/virgo/org.eclipse.virgo.kernel.users.properties.tpl"
        )
        self.confFinalPath = target_conf_dir + "org.eclipse.virgo.kernel.users.properties"
        user_name = CPVirgoAdminUserName()
        user_password = CPVirgoAdminUserPassword()
        self.paramsDictionary = {
            user_name.name: user_name,
            user_password.name: user_password
        }

    def process(self):
        return super(CUVirgoUsersProcessor, self).process()

    def get_param_from_key(self, key):
        return super(CUVirgoUsersProcessor, self).get_param_from_key(key)

    def get_params_keys_list(self):
        return super(CUVirgoUsersProcessor, self).get_params_keys_list()

    def set_key_param_value(self, key, value):
        return super(CUVirgoUsersProcessor, self).set_key_param_value(key, value)


class VirgoUsersSyringe:

    def __init__(self, target_conf_dir, silent):
        self.silent = silent
        self.virgoUsersCUProcessor = CUVirgoUsersProcessor(target_conf_dir)
        virgo_users_cujson = open("resources/configvalues/virgo/cuVirgoUsers.json")
        self.virgoUsersCUValues = json.load(virgo_users_cujson)
        virgo_users_cujson.close()

    def get_users_conf(self):
        return {
            'username': self.virgoUsersCUValues[CPVirgoAdminUserName.name],
            'password': self.virgoUsersCUValues[CPVirgoAdminUserPassword.name]
        }

    def shoot_builder(self):
        if not self.silent:
            virgo_admin_user_name_is_defined = False
            virgo_admin_user_name_default = self.virgoUsersCUValues[CPVirgoAdminUserName.name]
            virgo_admin_user_name_default_ui = "[default - " + virgo_admin_user_name_default + "] "
            while not virgo_admin_user_name_is_defined:
                username = input("%-- >> Define Virgo admin user name " + virgo_admin_user_name_default_ui + ": ")
                if username != "" and username is not None:
                    self.virgoUsersCUValues[CPVirgoAdminUserName.name] = username
                virgo_admin_user_name_is_defined = True

        self.virgoUsersCUProcessor.set_key_param_value(CPVirgoAdminUserName.name,
                                                    self.virgoUsersCUValues[CPVirgoAdminUserName.name])

        if not self.silent:
            virgo_admin_user_password_is_defined = False
            virgo_admin_user_password_default = self.virgoUsersCUValues[CPVirgoAdminUserPassword.name]

            while not virgo_admin_user_password_is_defined:
                password = getpass.getpass("%-- >> Define Virgo admin password : ")
                if password != "" and password is not None:
                    self.virgoUsersCUValues[CPVirgoAdminUserPassword.name] = password
                virgo_admin_user_password_is_defined = True

        self.virgoUsersCUProcessor.set_key_param_value(CPVirgoAdminUserPassword.name,
                                                    self.virgoUsersCUValues[CPVirgoAdminUserPassword.name])

    def inject(self):
        virgo_users_cujson = open("resources/configvalues/virgo/cuVirgoUsers.json", "w")
        json_str = json.dumps(self.virgoUsersCUValues, sort_keys=True, indent=4, separators=(',', ': '))
        virgo_users_cujson.write(json_str)
        virgo_users_cujson.close()
        self.virgoUsersCUProcessor.process()
