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


class CPVirgoKernelRegionOSGIConsoleSSHPort(AConfParamNotNone):

    name = "##kernelRegionSSHPort"
    description = "Virgo kernel region OSGI console ssh port"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPVirgoKernelRegionOSGIConsoleSSHPort, self).is_valid()


class CUVirgoKernelRegionOSGIConsoleProcessor(AConfUnit):

    def __init__(self, target_conf_dir):
        self.confUnitName = "Virgo Kernel Region OSGI Console"
        self.confTemplatePath = os.path.abspath(
            "resources/templates/virgo/org.eclipse.virgo.kernelregion.osgi.console.properties.tpl"
        )
        self.confFinalPath = target_conf_dir + "osgi.console.properties"
        kernel_osgi_console_ssh_port = CPVirgoKernelRegionOSGIConsoleSSHPort()
        self.paramsDictionary = {
            kernel_osgi_console_ssh_port.name: kernel_osgi_console_ssh_port
        }

    def process(self):
        return super(CUVirgoKernelRegionOSGIConsoleProcessor, self).process()

    def get_param_from_key(self, key):
        return super(CUVirgoKernelRegionOSGIConsoleProcessor, self).get_param_from_key(key)

    def get_params_keys_list(self):
        return super(CUVirgoKernelRegionOSGIConsoleProcessor, self).get_params_keys_list()

    def set_key_param_value(self, key, value):
        return super(CUVirgoKernelRegionOSGIConsoleProcessor, self).set_key_param_value(key, value)


class VirgoKernelRegionOSGIConsoleSyringe:

    def __init__(self, target_conf_dir, silent):
        self.silent = silent
        self.virgoKernelRegionOSGIConsoleCUProcessor = CUVirgoKernelRegionOSGIConsoleProcessor(target_conf_dir)
        virgo_kernel_region_osgi_console_cujson = open(
            "resources/configvalues/virgo/cuVirgoKernelRegionOSGIConsole.json"
        )
        self.virgoKernelRegionOSGIConsoleCUValues = json.load(virgo_kernel_region_osgi_console_cujson)
        virgo_kernel_region_osgi_console_cujson.close()

    def shoot_builder(self):
        if not self.silent:
            virgo_kernel_region_osgi_console_ssh_port_is_defined = False
            virgo_kernel_region_osgi_console_ssh_port_default = self.virgoKernelRegionOSGIConsoleCUValues[
                CPVirgoKernelRegionOSGIConsoleSSHPort.name
            ]
            virgo_kernel_region_osgi_console_ssh_port_default_ui = "[default - " + \
                str(virgo_kernel_region_osgi_console_ssh_port_default) + "] "

            kernel_osgi_ssh_port = virgo_kernel_region_osgi_console_ssh_port_default
            kernel_osgi_ssh_port_str = str(virgo_kernel_region_osgi_console_ssh_port_default)
            while not virgo_kernel_region_osgi_console_ssh_port_is_defined:
                kernel_osgi_ssh_port_str = input("%-- >> Define Virgo kernel region OSGI console ssh port " +
                                                 virgo_kernel_region_osgi_console_ssh_port_default_ui + ": ")
                if kernel_osgi_ssh_port_str != "" and kernel_osgi_ssh_port_str is not None:
                    try:
                        kernel_osgi_ssh_port = int(kernel_osgi_ssh_port_str)
                        if (kernel_osgi_ssh_port <= 0) and (kernel_osgi_ssh_port > 65535):
                            print("%-- !! Invalid DB port " + str(kernel_osgi_ssh_port) + ": not in port range")
                        else:
                            virgo_kernel_region_osgi_console_ssh_port_default = kernel_osgi_ssh_port_str
                            virgo_kernel_region_osgi_console_ssh_port_default_ui = "[default - " + \
                                                                                   kernel_osgi_ssh_port_str + "] "
                            virgo_kernel_region_osgi_console_ssh_port_is_defined = True
                    except ValueError:
                        print("%-- !! Invalid DB port " + kernel_osgi_ssh_port_str + " : not a number")
                else:
                    kernel_osgi_ssh_port = virgo_kernel_region_osgi_console_ssh_port_default
                    kernel_osgi_ssh_port_str = str(virgo_kernel_region_osgi_console_ssh_port_default)
                    virgo_kernel_region_osgi_console_ssh_port_is_defined = True

            self.virgoKernelRegionOSGIConsoleCUValues[
                CPVirgoKernelRegionOSGIConsoleSSHPort.name
            ] = kernel_osgi_ssh_port_str

        self.virgoKernelRegionOSGIConsoleCUProcessor.set_key_param_value(CPVirgoKernelRegionOSGIConsoleSSHPort.name,
                                                                      self.virgoKernelRegionOSGIConsoleCUValues[
                                                                          CPVirgoKernelRegionOSGIConsoleSSHPort.name
                                                                      ])

    def inject(self):
        virgo_kernel_region_osgi_console_cujson = open(
            "resources/configvalues/virgo/cuVirgoKernelRegionOSGIConsole.json", "w"
        )
        json_str = json.dumps(self.virgoKernelRegionOSGIConsoleCUValues,
                              sort_keys=True, indent=4, separators=(',', ': '))
        virgo_kernel_region_osgi_console_cujson.write(json_str)
        virgo_kernel_region_osgi_console_cujson.close()
        self.virgoKernelRegionOSGIConsoleCUProcessor.process()
