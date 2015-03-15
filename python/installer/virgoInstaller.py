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
import os
from subprocess import call, Popen
from time import sleep
from components.portal.portalProcessor import portalProcessor
from plugins.pluginInstaller import pluginInstaller, pluginProcessor
from core.virgo.virgoProcessor import virgoProcessor
from components.idm.idmProcessor import idmProcessor
from components.directory.directoryProcessor import directoryProcessor
from components.injector.injectorProcessor import injectorProcessor
from components.mapping.mappingProcessor import mappingProcessor

__author__ = 'mffrench'


def welcome():
    print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--")
    welcomeFile = open("resources/misc/welcome", "r")
    for line in welcomeFile:
        print(line, end='')


def license(silent):
    print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
    print("%-- By using this software you're agree with AGPLv3 license agreement.\n")
    if not silent:
        readlicense = input("%-- >> Do you want to read the AGPLv3 license agreement (yes or no - default no) ? ")
        if readlicense == "yes":
            licenseFile = open("COPYING.AGPL", "r")
            lineCounter = 0
            for line in licenseFile:
                if lineCounter < 30:
                    lineCounter += 1
                    print("%-- " + line, end='')
                else:
                    continueOrEscape = input("\n%-- >> Press enter to continue reading license or 'stop' to stop reading : ")
                    if continueOrEscape == "stop":
                        break
                    else:
                        lineCounter = 0
        else:
            print("%-- See http://www.gnu.org/licenses/ to know more about AGPLv3 license.\n")
    else:
        print("%-- See http://www.gnu.org/licenses/ to know more about AGPLv3 license.\n")


class virgoHomeDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values[0]
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("virgoHomeDir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            if os.access(prospective_dir, os.W_OK):
                if os.path.exists(prospective_dir + "/lib/org.eclipse.virgo.kernel.equinox.extensions_3.6.2.RELEASE.jar"):
                    setattr(namespace, self.dest, prospective_dir)
                else:
                    raise argparse.ArgumentTypeError("virgoHomeDir:{0} is not a valid virgo home dir".format(prospective_dir))
            else:
                raise argparse.ArgumentTypeError("virgoHomeDir:{0} is not a writable dir".format(prospective_dir))
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def parse():
    parser = argparse.ArgumentParser(description='Ariane virgo installer')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('virgoHome', help='Specify virgo home directory path', nargs=1, action=virgoHomeDir)
    group.add_argument('-a', '--autoconfigure', help='Configure Ariane environment with predefined value in $VIRGO_HOME/ariane/installer/resources/configvalues', action='store_true')
    group.add_argument('-c', '--configure', help='Configure Ariane environment', action='store_true')
    #todo: special action to validate the provided packages to install
    group.add_argument('-i', '--install', help='Install Ariane plugins packages', nargs='+')
    group.add_argument('-k', '--check', help="Check Ariane plugins packages", nargs="+")
    group.add_argument('-l', '--list', help='List installed Ariane plugins', action='store_true')
    #todo: special action to validate plugins id to uninstall
    group.add_argument('-u', '--uninstall', help='Uninstall Ariane plugin', nargs=2, metavar=("plugin_name", "plugin_version"))
    return parser.parse_args()

if __name__ == "__main__":
    args = parse()

    virgoHomeDirAbsPath = os.path.abspath(args.virgoHome)
    pwd = os.getcwd()
    os.chdir(virgoHomeDirAbsPath + "/ariane/installer")

    welcome()

    if args.autoconfigure:
        license(True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--")
        print("\n%-- Configuration of ariane virgo with auto mode [" + virgoHomeDirAbsPath + "]")
        virgoProcessor = virgoProcessor(virgoHomeDirAbsPath, True).process()
        idmProcessor = idmProcessor(virgoHomeDirAbsPath, True).process()
        portalProcess = portalProcessor(idmProcessor.idmDBConfig, virgoHomeDirAbsPath, True).process()
        mappingProcessor(idmProcessor.idmDBConfig, virgoHomeDirAbsPath, True).process()
        directoryProcessor = directoryProcessor(virgoHomeDirAbsPath, idmProcessor.idmDBConfig, True).process()
        injectorProcessor(virgoHomeDirAbsPath, idmProcessor.idmDBConfig, True).process()
        pluginProcessor = pluginProcessor(virgoHomeDirAbsPath, directoryProcessor.directoryDBConfig, idmProcessor.idmDBConfig, True).process()
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Ariane configuration is done !\n")

        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--")
        print("\n%-- Ariane deployment")
        classpath = virgoHomeDirAbsPath + "/ariane/installer/lib/mina-core-2.0.7.jar:" + \
                    virgoHomeDirAbsPath + "/ariane/installer/lib/slf4j-api-1.6.6.jar:" + \
                    virgoHomeDirAbsPath + "/ariane/installer/lib/sshd-core-0.11.0.jar:" + \
                    virgoHomeDirAbsPath + "/ariane/installer/lib/net.echinopsii.ariane.community.installer.tools-0.1.0.jar"
        mainClass = "net.echinopsii.ariane.community.install.tools.tools.sshcli"
        ssh = virgoProcessor.getUserRegionSSHParams()
        coreCmdsFilePath = virgoHomeDirAbsPath + "/ariane/installer/resources/virgoscripts/deploy-components.vsh"
        Popen([virgoHomeDirAbsPath + "/bin/startup.sh", "-clean"])
        sleep(30)
        call(["java", "-cp", classpath, mainClass, ssh.get('hostname'), ssh.get('port'), ssh.get('username'), ssh.get('password'), coreCmdsFilePath])
        sleep(60)
        call([virgoHomeDirAbsPath + "/bin/shutdown.sh"])
        if len(pluginProcessor.getDeployCommandsFiles()) != 0:
            sleep(20)
            Popen([virgoHomeDirAbsPath + "/bin/startup.sh"])
            sleep(60)
            for pluginCmdsFilePath in pluginProcessor.getDeployCommandsFiles():
                call(["java", "-cp", classpath, mainClass, ssh.get('hostname'), ssh.get('port'), ssh.get('username'), ssh.get('password'), pluginCmdsFilePath])
            sleep(60)
            call([virgoHomeDirAbsPath + "/bin/shutdown.sh"])
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Ariane deployment is done !\n")

    elif args.check:
        license(True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Check if provided Ariane plugin package(s) is/are valid :")
        for plugin in args.check:
            ret = pluginInstaller(virgoHomeDirAbsPath).checkPluginPackage(plugin)
            if ret is True:
                print("\n%-- Ariane plugin package " + plugin + " is valid !")
            else:
                print("\n%-- Ariane plugin package " + plugin + " is NOT valid ! Reason : " + ret)
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")

    elif args.configure:
        license(False)
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--")
        print("\n%-- Configuration of ariane distrib [" + virgoHomeDirAbsPath + "]")
        virgoProcessor = virgoProcessor(virgoHomeDirAbsPath, False).process()
        idmProcessor = idmProcessor(virgoHomeDirAbsPath, False).process()
        portalProcess = portalProcessor(idmProcessor.idmDBConfig, virgoHomeDirAbsPath, False).process()
        mappingProcessor(idmProcessor.idmDBConfig, virgoHomeDirAbsPath, False).process()
        directoryProcessor = directoryProcessor(virgoHomeDirAbsPath, idmProcessor.idmDBConfig, False).process()
        injectorProcessor(virgoHomeDirAbsPath, idmProcessor.idmDBConfig, False).process()
        pluginProcessor = pluginProcessor(virgoHomeDirAbsPath, directoryProcessor.directoryDBConfig, idmProcessor.idmDBConfig, False).process()
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Ariane configuration is done !\n")

        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--")
        print("\n%-- Ariane deployment")
        classpath = virgoHomeDirAbsPath + "/ariane/installer/lib/mina-core-2.0.7.jar:" + \
                    virgoHomeDirAbsPath + "/ariane/installer/lib/slf4j-api-1.6.6.jar:" + \
                    virgoHomeDirAbsPath + "/ariane/installer/lib/sshd-core-0.11.0.jar:" + \
                    virgoHomeDirAbsPath + "/ariane/installer/lib/net.echinopsii.ariane.community.installer.tools-0.1.0.jar"
        mainClass = "net.echinopsii.ariane.community.install.tools.tools.sshcli"
        ssh = virgoProcessor.getUserRegionSSHParams()
        coreCmdsFilePath = virgoHomeDirAbsPath + "/ariane/installer/resources/virgoscripts/deploy-components.vsh"
        Popen([virgoHomeDirAbsPath + "/bin/startup.sh", "-clean"])
        sleep(30)
        call(["java", "-cp", classpath, mainClass, ssh.get('hostname'), ssh.get('port'), ssh.get('username'), ssh.get('password'), coreCmdsFilePath])
        sleep(60)
        call([virgoHomeDirAbsPath + "/bin/shutdown.sh"])
        if len(pluginProcessor.getDeployCommandsFiles()) != 0:
            sleep(20)
            Popen([virgoHomeDirAbsPath + "/bin/startup.sh"])
            sleep(60)
            for pluginCmdsFilePath in pluginProcessor.getDeployCommandsFiles():
                call(["java", "-cp", classpath, mainClass, ssh.get('hostname'), ssh.get('port'), ssh.get('username'), ssh.get('password'), pluginCmdsFilePath])
            sleep(60)
            call([virgoHomeDirAbsPath + "/bin/shutdown.sh"])
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Ariane deployment is done !\n")

    elif args.install is not None:
        license(True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Install provided Ariane plugin package(s) is/are valid :")
        for plugin in args.install:
            pluginInstaller(virgoHomeDirAbsPath).installPluginPackage(plugin)
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")

    elif args.list:
        license(True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- List of installed Ariane plugin(s) in " + virgoHomeDirAbsPath + " :")
        pluginInstaller(virgoHomeDirAbsPath).listInstalledPluginPackages()
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")

    elif args.uninstall is not None:
        license(True)
        print("%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")
        print("%-- Uninstall Ariane plugin :")
        pluginInstaller(virgoHomeDirAbsPath).uninstallPluginPackage(args.uninstall[0], args.uninstall[1])
        print("\n%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--%--\n")

    os.chdir(pwd)
