#!/usr/bin/python3
#
# Ariane installer main
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
import argparse
import inspect
import json
import os
from subprocess import call, Popen
from time import sleep
from components.ComponentInstaller import ComponentProcessor
from core.bus.BusProcessor import BusProcessor
from plugins.PluginInstaller import PluginInstaller, PluginProcessor
from core.virgo.VirgoProcessor import VirgoProcessor


__author__ = 'mffrench'


def welcome():
    print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
          "%--%--%--%--%--%--%--%--")
    welcome_file = open("resources/misc/welcome", "r")
    for line in welcome_file:
        print(line, end='')


def ariane_license(ariane_version, silent):
    print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
          "%--%--%--%--%--%--%--%--\n")
    print("%-- Version: " + ariane_version + "\n")
    print("%-- By using this software you're agree with AGPLv3 license agreement.\n")
    if not silent:
        read_license = input("%-- >> Do you want to read the AGPLv3 license agreement (yes or no - default no) ? ")
        if read_license == "yes":
            license_file = open("COPYING.AGPL", "r")
            line_counter = 0
            for line in license_file:
                if line_counter < 30:
                    line_counter += 1
                    print("%-- " + line, end='')
                else:
                    continue_or_escape = input("\n%-- >> Press enter to continue reading license or 'stop' "
                                               "to stop reading : ")
                    if continue_or_escape == "stop":
                        break
                    else:
                        line_counter = 0
        else:
            print("%-- See http://www.gnu.org/licenses/ to know more about AGPLv3 license.\n")
    else:
        print("%-- See http://www.gnu.org/licenses/ to know more about AGPLv3 license.\n")


def parse(dep_type):
    parser = argparse.ArgumentParser(description='Ariane installer')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--autoconfigure', help='Configure Ariane environment with predefined value in '
                                                     '$INSTALL_HOME/ariane/installer/resources/configvalues',
                       action='store_true')
    group.add_argument('-c', '--configure', help='Configure Ariane environment', action='store_true')
    if dep_type == "mno" or dep_type == "frt":
        # todo: special action to validate the provided packages to install
        group.add_argument('-i', '--install', help='Install Ariane plugins packages', nargs='+')
        group.add_argument('-k', '--check', help="Check Ariane plugins packages", nargs="+")
        group.add_argument('-l', '--list', help='List installed Ariane plugins', action='store_true')
        # todo: special action to validate plugins id to uninstall
        group.add_argument('-u', '--uninstall', help='Uninstall Ariane plugin', nargs=2,
                           metavar=("plugin_name", "plugin_version"))
    return parser.parse_args()

if __name__ == "__main__":

    home_dir_abs_path = str(os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())
    )).split("/ariane/installer")[0])
    pwd = os.getcwd()
    os.chdir(home_dir_abs_path + "/ariane/installer")

    ctx_json = open(home_dir_abs_path + "/ariane/id.json")
    ctx_values = json.load(ctx_json)
    ctx_json.close()

    args = parse(ctx_values['deployment_type'])

    welcome()

    virgoProcessor = None
    if args.autoconfigure:
        ariane_license(ctx_values["version"], True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--")
        print("\n%-- Configuration of ariane with auto mode [" + home_dir_abs_path + "]")
        if ctx_values['deployment_type'] == "mno" or ctx_values['deployment_type'] == "frt":
            virgoProcessor = VirgoProcessor(home_dir_abs_path, True).process()
        busProcessor = BusProcessor(ctx_values["version"], ctx_values['deployment_type'], True)
        componentProcSgt = ComponentProcessor(home_dir_abs_path, busProcessor,
                                              ctx_values['deployment_type'], True).process()
        pluginProcSgt = PluginProcessor(home_dir_abs_path, ctx_values['deployment_type'],
                                        componentProcSgt.directoryDBConfig,
                                        componentProcSgt.idmDBConfig, True).process()
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Ariane configuration is done !\n")

        if virgoProcessor is not None:
            print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
                  "%--%--%--%--%--%--%--%--%--%--%--")
            print("\n%-- Ariane deployment")
            classpath = home_dir_abs_path + "/ariane/installer/lib/mina-core-2.0.7.jar:" + \
                home_dir_abs_path + "/ariane/installer/lib/slf4j-api-1.6.6.jar:" + \
                home_dir_abs_path + "/ariane/installer/lib/sshd-core-0.11.0.jar:" + \
                home_dir_abs_path + \
                "/ariane/installer/lib/net.echinopsii.ariane.community.installer.tools-0.1.0.jar"
            mainClass = "net.echinopsii.ariane.community.install.tools.tools.sshcli"
            ssh = virgoProcessor.get_user_region_ssh_params()
            core_cmds_file_path = home_dir_abs_path + "/ariane/installer/resources/virgoscripts/deploy-components.vsh"
            Popen([home_dir_abs_path + "/bin/startup.sh", "-clean"])
            sleep(30 if ctx_values['deployment_type'] == "mno" else 15)
            call(["java", "-cp", classpath, mainClass, ssh.get('hostname'), ssh.get('port'), ssh.get('username'),
                  ssh.get('password'), core_cmds_file_path])
            sleep(60 if ctx_values['deployment_type'] == "mno" else 30)
            call([home_dir_abs_path + "/bin/shutdown.sh"])
            if len(pluginProcSgt.get_deploy_commands_files()) != 0:
                sleep(20 if ctx_values['deployment_type'] == "mno" else 5)
                Popen([home_dir_abs_path + "/bin/startup.sh"])
                sleep(60 if ctx_values['deployment_type'] == "mno" else 15)
                for pluginCmdsFilePath in pluginProcSgt.get_deploy_commands_files():
                    call(["java", "-cp", classpath, mainClass, ssh.get('hostname'),
                          ssh.get('port'), ssh.get('username'),
                          ssh.get('password'), pluginCmdsFilePath])
                sleep(60 if ctx_values['deployment_type'] == "mno" else 15)
                call([home_dir_abs_path + "/bin/shutdown.sh"])
            print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
                  "%--%--%--%--%--%--%--%--%--%--%--\n")
            print("%-- Ariane deployment is done !\n")

    elif (ctx_values['deployment_type'] == "mno" or ctx_values['deployment_type'] == "frt") and args.check:
        ariane_license(ctx_values["version"], True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Check if provided Ariane plugin package(s) is/are valid :")
        for plugin in args.check:
            ret = PluginInstaller(home_dir_abs_path).check_plugin_package(plugin)
            if ret is True:
                print("\n%-- Ariane plugin package " + plugin + " is valid !")
            else:
                print("\n%-- Ariane plugin package " + plugin + " is NOT valid ! Reason : " + ret)
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")

    elif args.configure:
        ariane_license(ctx_values["version"], False)
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--")
        print("\n%-- Configuration of ariane distrib [" + home_dir_abs_path + "]")
        if ctx_values['deployment_type'] == "mno" or ctx_values['deployment_type'] == "frt":
            virgoProcessor = VirgoProcessor(home_dir_abs_path, False).process()
        busProcessor = BusProcessor(ctx_values["version"], ctx_values['deployment_type'], False)
        componentProcSgt = ComponentProcessor(home_dir_abs_path, busProcessor,
                                              ctx_values['deployment_type'], False).process()
        pluginProcSgt = PluginProcessor(home_dir_abs_path, ctx_values['deployment_type'],
                                        componentProcSgt.directoryDBConfig,
                                        componentProcSgt.idmDBConfig, False).process()
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Ariane configuration is done !\n")

        if virgoProcessor is not None:
            print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
                  "%--%--%--%--%--%--%--%--%--%--%--")
            print("\n%-- Ariane deployment")
            classpath = home_dir_abs_path + "/ariane/installer/lib/mina-core-2.0.7.jar:" + \
                home_dir_abs_path + "/ariane/installer/lib/slf4j-api-1.6.6.jar:" + \
                home_dir_abs_path + "/ariane/installer/lib/sshd-core-0.11.0.jar:" + \
                home_dir_abs_path + "/ariane/installer/lib/net.echinopsii.ariane.community.installer.tools-0.1.0.jar"
            mainClass = "net.echinopsii.ariane.community.install.tools.tools.sshcli"
            ssh = virgoProcessor.get_user_region_ssh_params()
            core_cmds_file_path = home_dir_abs_path + "/ariane/installer/resources/virgoscripts/deploy-components.vsh"
            Popen([home_dir_abs_path + "/bin/startup.sh", "-clean"])
            sleep(30 if ctx_values['deployment_type'] == "mno" else 15)
            call(["java", "-cp", classpath, mainClass, ssh.get('hostname'), ssh.get('port'), ssh.get('username'),
                  ssh.get('password'), core_cmds_file_path])
            sleep(60 if ctx_values['deployment_type'] == "mno" else 15)
            call([home_dir_abs_path + "/bin/shutdown.sh"])
            if len(pluginProcSgt.get_deploy_commands_files()) != 0:
                sleep(20 if ctx_values['deployment_type'] == "mno" else 5)
                Popen([home_dir_abs_path + "/bin/startup.sh"])
                sleep(60 if ctx_values['deployment_type'] == "mno" else 15)
                for pluginCmdsFilePath in pluginProcSgt.get_deploy_commands_files():
                    call(["java", "-cp", classpath, mainClass, ssh.get('hostname'),
                          ssh.get('port'), ssh.get('username'),
                          ssh.get('password'), pluginCmdsFilePath])
                sleep(60 if ctx_values['deployment_type'] == "mno" else 15)
                call([home_dir_abs_path + "/bin/shutdown.sh"])
            print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
                  "%--%--%--%--%--%--%--%--%--%--%--\n")
            print("%-- Ariane deployment is done !\n")

    elif (ctx_values['deployment_type'] == "mno" or ctx_values['deployment_type'] == "frt") and \
            args.install is not None:
        ariane_license(ctx_values["version"], True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Install provided Ariane plugin package(s) is/are valid :")
        for plugin in args.install:
            PluginInstaller(home_dir_abs_path).install_plugin_package(plugin)
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")

    elif (ctx_values['deployment_type'] == "mno" or ctx_values['deployment_type'] == "frt") and args.list:
        ariane_license(ctx_values["version"], True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- List of installed Ariane plugin(s) in " + home_dir_abs_path + " :")
        PluginInstaller(home_dir_abs_path).list_installed_plugin_packages()
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")

    elif (ctx_values['deployment_type'] == "mno" or ctx_values['deployment_type'] == "frt") and \
            args.uninstall is not None:
        ariane_license(ctx_values["version"], True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")
        print("%-- Uninstall Ariane plugin :")
        PluginInstaller(home_dir_abs_path).uninstall_plugin_package(args.uninstall[0], args.uninstall[1])
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--"
              "%--%--%--%--%--%--%--%--%--\n")

    os.chdir(pwd)
