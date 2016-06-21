# installer - virgo user region osgi console
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
from tools.AConfParamNotNone import AConfParamNotNone
from tools.AConfUnit import AConfUnit

__author__ = 'mffrench'


class CPVirgoUserRegionOSGIConsoleSSHPort(AConfParamNotNone):

    name = "##userRegionSSHPort"
    description = "Virgo user region OSGI console ssh port"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPVirgoUserRegionOSGIConsoleSSHPort, self).is_valid()


class CUVirgoUserRegionOSGIConsoleProcessor(AConfUnit):

    def __init__(self, target_conf_dir):
        self.confUnitName = "Virgo User Region OSGI Console"
        self.confTemplatePath = os.path.abspath(
            "resources/templates/virgo/org.eclipse.virgo.userregion.osgi.console.properties.tpl"
        )
        self.confFinalPath = target_conf_dir + "osgi.console.properties"
        user_osgi_console_ssh_port = CPVirgoUserRegionOSGIConsoleSSHPort()
        self.paramsDictionary = {
            user_osgi_console_ssh_port.name: user_osgi_console_ssh_port
        }

    def process(self):
        return super(CUVirgoUserRegionOSGIConsoleProcessor, self).process()

    def get_param_from_key(self, key):
        return super(CUVirgoUserRegionOSGIConsoleProcessor, self).get_param_from_key(key)

    def get_params_keys_list(self):
        return super(CUVirgoUserRegionOSGIConsoleProcessor, self).get_params_keys_list()

    def set_key_param_value(self, key, value):
        return super(CUVirgoUserRegionOSGIConsoleProcessor, self).set_key_param_value(key, value)


class VirgoUserRegionOSGIConsoleSyringe:

    def __init__(self, target_conf_dir, silent):
        self.silent = silent
        self.virgoUserRegionOSGIConsoleCUProcessor = CUVirgoUserRegionOSGIConsoleProcessor(target_conf_dir)
        virgo_user_region_osgi_console_cujson = open("resources/configvalues/virgo/cuVirgoUserRegionOSGIConsole.json")
        self.virgoUserRegionOSGIConsoleCUValues = json.load(virgo_user_region_osgi_console_cujson)
        virgo_user_region_osgi_console_cujson.close()

    def get_user_region_ssh_params(self):
        return {
            'hostname': 'localhost',
            'port': self.virgoUserRegionOSGIConsoleCUValues[CPVirgoUserRegionOSGIConsoleSSHPort.name]
        }

    def shoot_builder(self):
        if not self.silent:
            virgo_user_region_osgi_console_ssh_port_is_defined = False
            virgo_user_region_osgi_console_ssh_port_default = self.virgoUserRegionOSGIConsoleCUValues[
                CPVirgoUserRegionOSGIConsoleSSHPort.name
            ]
            virgo_user_region_osgi_console_ssh_port_default_ui = "[default - " + \
                                                                 str(virgo_user_region_osgi_console_ssh_port_default) + \
                                                                 "] "

            user_osgi_ssh_port = 0
            user_osgi_ssh_port_str = "0"
            while not virgo_user_region_osgi_console_ssh_port_is_defined:
                user_osgi_ssh_port_str = input("%-- >> Define Virgo user region OSGI console ssh port " +
                                               virgo_user_region_osgi_console_ssh_port_default_ui + ": ")
                if user_osgi_ssh_port_str != "" and user_osgi_ssh_port_str is not None:
                    try:
                        user_osgi_ssh_port = int(user_osgi_ssh_port_str)
                        if (user_osgi_ssh_port <= 0) and (user_osgi_ssh_port > 65535):
                            print("%-- !! Invalid DB port " + str(user_osgi_ssh_port) + ": not in port range")
                        else:
                            virgo_user_region_osgi_console_ssh_port_default = user_osgi_ssh_port_str
                            virgo_user_region_osgi_console_ssh_port_default_ui = "[default - " + user_osgi_ssh_port_str \
                                                                                 + "] "
                            virgo_user_region_osgi_console_ssh_port_is_defined = True
                    except ValueError:
                        print("%-- !! Invalid DB port " + user_osgi_ssh_port_str + " : not a number")
                else:
                    user_osgi_ssh_port = virgo_user_region_osgi_console_ssh_port_default
                    user_osgi_ssh_port_str = str(virgo_user_region_osgi_console_ssh_port_default)
                    virgo_user_region_osgi_console_ssh_port_is_defined = True

            self.virgoUserRegionOSGIConsoleCUValues[CPVirgoUserRegionOSGIConsoleSSHPort.name] = user_osgi_ssh_port_str

        self.virgoUserRegionOSGIConsoleCUProcessor.set_key_param_value(CPVirgoUserRegionOSGIConsoleSSHPort.name,
                                                                    self.virgoUserRegionOSGIConsoleCUValues[
                                                                        CPVirgoUserRegionOSGIConsoleSSHPort.name
                                                                    ])

    def inject(self):
        virgo_user_region_osgi_console_cujson = open(
            "resources/configvalues/virgo/cuVirgoUserRegionOSGIConsole.json", "w"
        )
        json_str = json.dumps(self.virgoUserRegionOSGIConsoleCUValues, sort_keys=True, indent=4, separators=(',', ': '))
        virgo_user_region_osgi_console_cujson.write(json_str)
        virgo_user_region_osgi_console_cujson.close()
        self.virgoUserRegionOSGIConsoleCUProcessor.process()