# installer ariane bus processor
#
# Copyright (C) 2016 Mathilde Ffrench
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
import platform
import socket
from tools.AConfParamNotNone import AConfParamNotNone
from tools.AConfUnit import AConfUnit

__author__ = 'mffrench'

class CPBusMoMProvider(AConfParamNotNone):

    name = "##MCLI_IMPL"
    description = "Ariane MoM provider type (NATS or RabbitMQ)"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMProvider, self).is_valid()


class CPBusMoMHostFQDN(AConfParamNotNone):

    name = "##MHOST_FQDN"
    description = "Ariane MoM Host FQDN"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMHostFQDN, self).is_valid()


class CPBusMoMHostPort(AConfParamNotNone):

    name = "##MHOST_PORT"
    description = "Ariane MoM Host Port"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMHostPort, self).is_valid()


class CPBusMoMHostUser(AConfParamNotNone):

    name = "##MHOST_USER"
    description = "Ariane MoM Host User"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMHostUser, self).is_valid()


class CPBusMoMHostPasswd(AConfParamNotNone):

    name = "##MHOST_PASSWD"
    description = "Ariane MoM Host Password"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMHostPasswd, self).is_valid()


class CPBusMoMCliRBQVersion(AConfParamNotNone):

    name = "##MCLI_RBQ_VERSION"
    description = "Ariane MoM RabbitMQ Client Version"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMCliRBQVersion, self).is_valid()


class CPBusMoMHostRBQVhost(AConfParamNotNone):

    name = "##MHOST_RBQ_VHOST"
    description = "Ariane MoM Host RabbitMQ Vhost"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMHostRBQVhost, self).is_valid()


class CPBusMoMCliNATSname(AConfParamNotNone):

    name = "##MCLI_NATS_NAME"
    description = "Ariane MoM Client Version"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusMoMCliNATSname, self).is_valid()


class CPBusArianeFQDN(AConfParamNotNone):

    name = "##ARIANE_FQDN"
    description = "Ariane server FQDN"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusArianeFQDN, self).is_valid()


class CPBusArianeHost(AConfParamNotNone):

    name = "##ARIANE_HOST"
    description = "Ariane server hostname"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusArianeHost, self).is_valid()


class CPBusArianeOPST(AConfParamNotNone):

    name = "##ARIANE_OPS_TEAM"
    description = "Ariane OPS team"
    hide = False

    def __init__(self):
        self.value = None

    def is_valid(self):
        return super(CPBusArianeOPST, self).is_valid()


class CUBusProcessor(AConfUnit):

    def __init__(self):
        self.confUnitName = "Bus"
        self.confTemplatePath = None
        self.confFinalPath = None

        bus_mom_provider = CPBusMoMProvider()
        bus_mom_host_fqdn = CPBusMoMHostFQDN()
        bus_mom_host_port = CPBusMoMHostPort()
        bus_mom_host_user = CPBusMoMHostUser()
        bus_mom_host_passwd = CPBusMoMHostPasswd()
        bus_mom_host_rbq_vhost = CPBusMoMHostRBQVhost()
        bus_mom_cli_rbq_version = CPBusMoMCliRBQVersion()
        bus_ariane_fqdn = CPBusArianeFQDN()
        bus_ariane_host = CPBusArianeHost()
        bus_ariane_opst = CPBusArianeOPST()

        self.paramsDictionary = {
            bus_mom_provider.name: bus_mom_provider,
            bus_mom_cli_rbq_version.name: bus_mom_cli_rbq_version,
            bus_mom_host_fqdn.name: bus_mom_host_fqdn,
            bus_mom_host_port.name: bus_mom_host_port,
            bus_mom_host_user.name: bus_mom_host_user,
            bus_mom_host_passwd.name: bus_mom_host_passwd,
            bus_mom_host_rbq_vhost.name: bus_mom_host_rbq_vhost,
            bus_ariane_fqdn.name: bus_ariane_fqdn,
            bus_ariane_host.name: bus_ariane_host,
            bus_ariane_opst.name: bus_ariane_opst
        }

    def process(self):
        return super(CUBusProcessor, self).process()

    def get_param_from_key(self, key):
        return super(CUBusProcessor, self).get_param_from_key(key)

    def get_params_keys_list(self):
        return super(CUBusProcessor, self).get_params_keys_list()

    def set_key_param_value(self, key, value):
        return super(CUBusProcessor, self).set_key_param_value(key, value)


class BusSyringe:

    def __init__(self, dist_version, silent):
        self.silent = silent
        self.busCUProcessor = CUBusProcessor()
        bus_cu_json = open("resources/configvalues/bus/cuBus.json")
        self.busCUValues = json.load(bus_cu_json)
        self.default_values_injected = False
        self.dist_version = dist_version
        bus_cu_json.close()

    def shoot_builder(self):
        bus_connection_defined = False
        for key in self.busCUProcessor.get_params_keys_list():

            if (key == CPBusMoMHostFQDN.name or key == CPBusMoMHostPort.name or
                key == CPBusMoMHostUser.name or key == CPBusMoMHostPasswd.name) \
                    and not bus_connection_defined:

                mom_provider_default = self.busCUValues[CPBusMoMProvider.name]
                if mom_provider_default == "net.echinopsii.ariane.community.messaging.rabbitmq.Client":
                    mom_provider_default_ui = "[default - RabbitMQ] "
                elif mom_provider_default == "net.echinopsii.ariane.community.messaging.nats.Client":
                    mom_provider_default_ui = "[default - NATS] "
                else:
                    mom_provider_default_ui = "[default - NATS] "
                    mom_provider_default = "net.echinopsii.ariane.community.messaging.nats.Client"
                mom_provider = mom_provider_default

                mom_host_fqdn_default = self.busCUValues[CPBusMoMHostFQDN.name]
                mom_host_fqdn_default_ui = "[default - " + mom_host_fqdn_default + "] "
                mom_host_fqdn = mom_host_fqdn_default

                if mom_provider == "net.echinopsii.ariane.community.messaging.rabbitmq.Client":
                    mom_host_port_default = self.busCUValues[CPBusMoMHostPort.name]
                    mom_host_port_default_ui = "[default - " + mom_host_port_default + "] "
                    mom_host_port = int(mom_host_port_default)
                else:
                    mom_host_port_default = str(4222)
                    mom_host_port_default_ui = "[default - " + mom_host_port_default + "] "
                    mom_host_port = int(mom_host_port_default)

                mom_host_user_default = self.busCUValues[CPBusMoMHostUser.name]
                mom_host_user_default_ui = "[default - " + mom_host_user_default + "] "
                mom_host_user = mom_host_user_default

                mom_host_password_default = self.busCUValues[CPBusMoMHostPasswd.name]
                mom_host_password = mom_host_password_default

                mom_host_rbmq_vhost_default = self.busCUValues[CPBusMoMHostRBQVhost.name]
                mom_host_rbmq_vhost_default_ui = "[default - " + mom_host_rbmq_vhost_default + "] "
                mom_host_rbmq_vhost = mom_host_rbmq_vhost_default

                ariane_ops_team_default = self.busCUValues[CPBusArianeOPST.name]
                ariane_ops_team_default_ui = "[default - " + ariane_ops_team_default + "] "
                ariane_ops_team = ariane_ops_team_default

                while not bus_connection_defined:

                    if not self.silent:
                        mom_provider_is_valid = False
                        while not mom_provider_is_valid:
                            mom_provider_code = input("%-- >> Define Bus provider type "
                                                      "(enter 1 for NATS or 2 for RabbitMQ) " + mom_provider_default_ui
                                                      + ": ")
                            if mom_provider_code == "1":
                                mom_provider = "net.echinopsii.ariane.community.messaging.nats.Client"
                                mom_host_port_default = str(4222)
                                mom_host_port_default_ui = "[default - " + mom_host_port_default + "] "
                                mom_host_port = int(mom_host_port_default)
                                mom_provider_is_valid = True
                            elif mom_provider_code == "2":
                                mom_provider = "net.echinopsii.ariane.community.messaging.rabbitmq.Client"
                                mom_host_port_default = str(5672)
                                mom_host_port_default_ui = "[default - " + mom_host_port_default + "] "
                                mom_host_port = int(mom_host_port_default)
                                mom_provider_is_valid = True
                            elif mom_provider_code is None or not mom_provider_code:
                                mom_provider = "net.echinopsii.ariane.community.messaging.nats.Client"
                                mom_host_port_default = str(4222)
                                mom_host_port_default_ui = "[default - " + mom_host_port_default + "] "
                                mom_host_port = int(mom_host_port_default)
                                mom_provider_is_valid = True
                            else:
                                print("%-- !! Invalid Bus provider (" + str(mom_host_port) +
                                      ") : you must enter 1 (for NATS) or 2 (for RabbitMQ)")
                        mom_provider_default = mom_provider

                    if not self.silent:
                        mom_user_fqdn = input("%-- >> Define Bus User " + mom_host_user_default_ui + ": ")
                        if mom_user_fqdn == "" or mom_user_fqdn is None:
                            mom_host_user = mom_host_user_default
                        else:
                            mom_host_user_default_ui = "[default - " + mom_host_user + "] "
                            mom_host_user_default = mom_host_user

                    if not self.silent:
                        mom_host_password = getpass.getpass("%-- >> Define Bus Password: ")
                        while mom_host_password == "" or mom_host_password is None:
                            mom_host_password = getpass.getpass("%-- >> Define Bus Password: ")
                        mom_host_password_default = mom_host_password

                    if not self.silent:
                        mom_host_fqdn = input("%-- >> Define Bus server FQDN " + mom_host_fqdn_default_ui + ": ")
                        if mom_host_fqdn == "" or mom_host_fqdn is None:
                            mom_host_fqdn = mom_host_fqdn_default
                        else:
                            mom_host_fqdn_default_ui = "[default - " + mom_host_fqdn + "] "
                            mom_host_fqdn_default = mom_host_fqdn

                    if not self.silent:
                        mom_port_is_valid = False
                        mom_port_str = ""
                        while not mom_port_is_valid:
                            mom_host_port = 0
                            mom_port_str = input("%-- >> Define Bus server port " + mom_host_port_default_ui + ": ")
                            if mom_port_str == "" or mom_port_str is None:
                                mom_port_str = mom_host_port_default
                                mom_host_port = int(mom_host_port_default)
                                mom_port_is_valid = True
                            else:
                                try:
                                    mom_host_port = int(mom_port_str)
                                    if (mom_host_port <= 0) or (mom_host_port > 65535):
                                        print("%-- !! Invalid Bus port " + str(mom_host_port) + ": not in port range")
                                    else:
                                        mom_host_port_default_ui = "[default - " + mom_port_str + "] "
                                        mom_host_port_default = mom_port_str
                                        mom_port_is_valid = True
                                except ValueError:
                                    print("%-- !! Invalid Bus port " + mom_port_str + " : not a number")

                    if not self.silent and mom_provider == "net.echinopsii.ariane.community.messaging.rabbitmq.Client":
                        mom_vhost_is_valid = False
                        mom_host_rbmq_vhost = ""
                        while not mom_vhost_is_valid:
                            mom_host_rbmq_vhost = input("%-- >> Define Bus RabbitMQ vhost " +
                                                        mom_host_rbmq_vhost_default_ui + ": ")
                            if mom_host_rbmq_vhost != "":
                                mom_vhost_is_valid = True
                                mom_host_rbmq_vhost_default = mom_host_rbmq_vhost
                                mom_host_rbmq_vhost_default_ui = "[default - " + mom_host_rbmq_vhost + "] "
                            elif mom_host_rbmq_vhost_default != "":
                                mom_host_rbmq_vhost = mom_host_rbmq_vhost_default
                                mom_vhost_is_valid = True

                    bus_connection_defined = True

                if not self.silent:
                    ariane_ops_team = input("%-- >> Define Ariane OPS team name " + ariane_ops_team_default_ui + ": ")
                    if ariane_ops_team == "" or ariane_ops_team is None:
                        ariane_ops_team = ariane_ops_team
                    else:
                        ariane_ops_team_default_ui = "[default - " + ariane_ops_team + "] "
                        ariane_ops_team_default = ariane_ops_team

                self.busCUProcessor.set_key_param_value(CPBusMoMProvider.name, mom_provider)
                self.busCUProcessor.set_key_param_value(CPBusMoMHostFQDN.name, mom_host_fqdn)
                self.busCUProcessor.set_key_param_value(CPBusMoMHostPort.name, mom_host_port)
                self.busCUProcessor.set_key_param_value(CPBusMoMHostUser.name, mom_host_user)
                self.busCUProcessor.set_key_param_value(CPBusMoMHostPasswd.name, mom_host_password)
                self.busCUProcessor.set_key_param_value(CPBusMoMHostRBQVhost.name, mom_host_rbmq_vhost)
                self.busCUProcessor.set_key_param_value(CPBusArianeFQDN.name, socket.getfqdn())
                self.busCUProcessor.set_key_param_value(CPBusArianeHost.name, platform.node())
                self.busCUProcessor.set_key_param_value(CPBusArianeOPST.name, ariane_ops_team)

            elif key == CPBusMoMCliRBQVersion.name:
                self.busCUProcessor.set_key_param_value(CPBusMoMCliRBQVersion.name, self.dist_version)

            elif key == CPBusMoMCliNATSname.name:
                self.busCUProcessor.set_key_param_value(CPBusMoMCliNATSname.name, "Ariane")

    def set_conf_template_path(self, conf_template_path):
        self.busCUProcessor.confTemplatePath = os.path.abspath(conf_template_path)

    def set_conf_final_path(self, conf_final_path):
        self.busCUProcessor.confFinalPath = conf_final_path

    def inject(self):
        if not self.default_values_injected:
            bus_cu_json = open("resources/configvalues/bus/cuBus.json", "w")
            json_str = json.dumps(self.busCUValues, sort_keys=True, indent=4, separators=(',', ': '))
            bus_cu_json.write(json_str)
            bus_cu_json.close()
            self.default_values_injected = True
        # print(str(self.busCUProcessor.confTemplatePath))
        # print(str(self.busCUProcessor.confFinalPath))
        if self.busCUProcessor.confTemplatePath is not None and self.busCUProcessor.confFinalPath is not None:
            self.busCUProcessor.process()
