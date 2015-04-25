# installer - virgo kernel region osgi console
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


class cpVirgoKernelRegionOSGIConsoleSSHPort(AConfParamNotNone):

    name = "##kernelRegionSSHPort"
    description = "Virgo kernel region OSGI console ssh port"
    hide = False

    def __init__(self):
        self.value = None


class cuVirgoKernelRegionOSGIConsoleProcessor(AConfUnit):

    def __init__(self, targetConfDir):
        self.confUnitName = "Virgo Kernel Region OSGI Console"
        self.confTemplatePath = os.path.abspath("resources/templates/virgo/org.eclipse.virgo.kernelregion.osgi.console.properties.tpl")
        self.confFinalPath = targetConfDir + "osgi.console.properties"
        kernelOSGIConsoleSSHPort = cpVirgoKernelRegionOSGIConsoleSSHPort()
        self.paramsDictionary = {
            kernelOSGIConsoleSSHPort.name: kernelOSGIConsoleSSHPort
        }

class virgoKernelRegionOSGIConsoleSyringe:

    def __init__(self, targetConfDif, silent):
        self.silent = silent
        self.virgoKernelRegionOSGIConsoleCUProcessor = cuVirgoKernelRegionOSGIConsoleProcessor(targetConfDif)
        virgoKernelRegionOSGIConsoleCUJSON = open("resources/configvalues/virgo/cuVirgoKernelRegionOSGIConsole.json")
        self.virgoKernelRegionOSGIConsoleCUValues = json.load(virgoKernelRegionOSGIConsoleCUJSON)
        virgoKernelRegionOSGIConsoleCUJSON.close()

    def shootBuilder(self):
        if not self.silent:
            virgoKernelRegionOSGIConsoleSSHPortIsDefined = False
            virgoKernelRegionOSGIConsoleSSHPortDefault   = self.virgoKernelRegionOSGIConsoleCUValues[cpVirgoKernelRegionOSGIConsoleSSHPort.name]
            virgoKernelRegionOSGIConsoleSSHPortDefaultUI = "[default - " + str(virgoKernelRegionOSGIConsoleSSHPortDefault) + "] "

            kernelOSGISSHPort = virgoKernelRegionOSGIConsoleSSHPortDefault
            kernelOSGISSHPortStr = str(virgoKernelRegionOSGIConsoleSSHPortDefault)
            while not virgoKernelRegionOSGIConsoleSSHPortIsDefined:
                kernelOSGISSHPortStr = input("%-- >> Define Virgo kernel region OSGI console ssh port " + virgoKernelRegionOSGIConsoleSSHPortDefaultUI + ": ")
                if kernelOSGISSHPortStr != "" and kernelOSGISSHPortStr is not None:
                    try:
                        kernelOSGISSHPort = int(kernelOSGISSHPortStr)
                        if (kernelOSGISSHPort <= 0) and (kernelOSGISSHPort > 65535):
                            print("%-- !! Invalid DB port " + str(kernelOSGISSHPort) + ": not in port range")
                        else:
                            virgoKernelRegionOSGIConsoleSSHPortDefault = kernelOSGISSHPortStr
                            virgoKernelRegionOSGIConsoleSSHPortDefaultUI = "[default - " + kernelOSGISSHPortStr + "] "
                            virgoKernelRegionOSGIConsoleSSHPortIsDefined = True
                    except ValueError:
                        print("%-- !! Invalid DB port " + kernelOSGISSHPortStr + " : not a number")
                else:
                    kernelOSGISSHPort = virgoKernelRegionOSGIConsoleSSHPortDefault
                    kernelOSGISSHPortStr = str(virgoKernelRegionOSGIConsoleSSHPortDefault)
                    virgoKernelRegionOSGIConsoleSSHPortIsDefined = True

            self.virgoKernelRegionOSGIConsoleCUValues[cpVirgoKernelRegionOSGIConsoleSSHPort.name] = kernelOSGISSHPortStr

        self.virgoKernelRegionOSGIConsoleCUProcessor.setKeyParamValue(cpVirgoKernelRegionOSGIConsoleSSHPort.name, self.virgoKernelRegionOSGIConsoleCUValues[cpVirgoKernelRegionOSGIConsoleSSHPort.name])

    def inject(self):
        virgoKernelRegionOSGIConsoleCUJSON = open("resources/configvalues/virgo/cuVirgoKernelRegionOSGIConsole.json","w")
        jsonStr = json.dumps(self.virgoKernelRegionOSGIConsoleCUValues, sort_keys=True, indent=4, separators=(',', ': '))
        virgoKernelRegionOSGIConsoleCUJSON.write(jsonStr)
        virgoKernelRegionOSGIConsoleCUJSON.close()
        self.virgoKernelRegionOSGIConsoleCUProcessor.process()