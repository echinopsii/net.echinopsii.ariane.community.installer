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


class cpVirgoUserRegionOSGIConsoleSSHPort(AConfParamNotNone):

    name = "##userRegionSSHPort"
    description = "Virgo user region OSGI console ssh port"
    hide = False

    def __init__(self):
        self.value = None


class cuVirgoUserRegionOSGIConsoleProcessor(AConfUnit):

    def __init__(self, targetConfDir):
        self.confUnitName = "Virgo User Region OSGI Console"
        self.confTemplatePath = os.path.abspath("resources/templates/virgo/org.eclipse.virgo.userregion.osgi.console.properties.tpl")
        self.confFinalPath = targetConfDir + "osgi.console.properties"
        userOSGIConsoleSSHPort = cpVirgoUserRegionOSGIConsoleSSHPort()
        self.paramsDictionary = {
            userOSGIConsoleSSHPort.name: userOSGIConsoleSSHPort
        }

class virgoUserRegionOSGIConsoleSyringe:

    def __init__(self, targetConfDif, silent):
        self.silent = silent
        self.virgoUserRegionOSGIConsoleCUProcessor = cuVirgoUserRegionOSGIConsoleProcessor(targetConfDif)
        virgoUserRegionOSGIConsoleCUJSON = open("resources/configvalues/virgo/cuVirgoUserRegionOSGIConsole.json")
        self.virgoUserRegionOSGIConsoleCUValues = json.load(virgoUserRegionOSGIConsoleCUJSON)
        virgoUserRegionOSGIConsoleCUJSON.close()

    def getUserRegionSSHParams(self):
        return {
            'hostname': 'localhost',
            'port': self.virgoUserRegionOSGIConsoleCUValues[cpVirgoUserRegionOSGIConsoleSSHPort.name]
        }

    def shootBuilder(self):
        if not self.silent:
            virgoUserRegionOSGIConsoleSSHPortIsDefined = False
            virgoUserRegionOSGIConsoleSSHPortDefault   = self.virgoUserRegionOSGIConsoleCUValues[cpVirgoUserRegionOSGIConsoleSSHPort.name]
            virgoUserRegionOSGIConsoleSSHPortDefaultUI = "[default - " + str(virgoUserRegionOSGIConsoleSSHPortDefault) + "] "

            userOSGISSHPort = 0
            userOSGISSHPortStr = "0"
            while not virgoUserRegionOSGIConsoleSSHPortIsDefined:
                userOSGISSHPortStr = input("%-- >> Define Virgo user region OSGI console ssh port " + virgoUserRegionOSGIConsoleSSHPortDefaultUI + ": ")
                if userOSGISSHPortStr != "" and userOSGISSHPortStr is not None:
                    try:
                        userOSGISSHPort = int(userOSGISSHPortStr)
                        if (userOSGISSHPort <= 0) and (userOSGISSHPort > 65535):
                            print("%-- !! Invalid DB port " + str(userOSGISSHPort) + ": not in port range")
                        else:
                            virgoUserRegionOSGIConsoleSSHPortDefault = userOSGISSHPortStr
                            virgoUserRegionOSGIConsoleSSHPortDefaultUI = "[default - " + userOSGISSHPortStr + "] "
                            virgoUserRegionOSGIConsoleSSHPortIsDefined = True
                    except ValueError:
                        print("%-- !! Invalid DB port " + userOSGISSHPortStr + " : not a number")
                else:
                    userOSGISSHPort = virgoUserRegionOSGIConsoleSSHPortDefault
                    userOSGISSHPortStr = str(virgoUserRegionOSGIConsoleSSHPortDefault)
                    virgoUserRegionOSGIConsoleSSHPortIsDefined = True

            self.virgoUserRegionOSGIConsoleCUValues[cpVirgoUserRegionOSGIConsoleSSHPort.name] = userOSGISSHPortStr

        self.virgoUserRegionOSGIConsoleCUProcessor.setKeyParamValue(cpVirgoUserRegionOSGIConsoleSSHPort.name, self.virgoUserRegionOSGIConsoleCUValues[cpVirgoUserRegionOSGIConsoleSSHPort.name])

    def inject(self):
        virgoUserRegionOSGIConsoleCUJSON = open("resources/configvalues/virgo/cuVirgoUserRegionOSGIConsole.json", "w")
        jsonStr = json.dumps(self.virgoUserRegionOSGIConsoleCUValues, sort_keys=True, indent=4, separators=(',', ': '))
        virgoUserRegionOSGIConsoleCUJSON.write(jsonStr)
        virgoUserRegionOSGIConsoleCUJSON.close()
        self.virgoUserRegionOSGIConsoleCUProcessor.process()