# CC addon installer main
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
import fnmatch
import os
import shutil
import tempfile
import zipfile
from tools.AddonDesc import addonDesc

__author__ = 'mffrench'


class addonInstaller:

    def __init__(self, virgoHomePath):
        self.virgoHomePath = virgoHomePath

    def checkAddonPackage(self, addonPackagePath):
        if os.path.exists(addonPackagePath) and zipfile.is_zipfile(addonPackagePath):
            tmpTestDir = tempfile.mkdtemp()
            pwd = os.getcwd()
            os.chdir(tmpTestDir)
            addonZip = zipfile.ZipFile(addonPackagePath)
            addonZip.extractall()

            addonInstallerDir = tmpTestDir + "/ariane/installer/addons"
            if os.path.exists(addonInstallerDir) and os.path.isdir(addonInstallerDir):
                for file in os.listdir(addonInstallerDir):
                    if os.path.isdir(addonInstallerDir + "/" + file) and os.path.exists(addonInstallerDir + "/" + file + "/arianeaddondesc.json"):
                        try:
                            addonDesc(addonInstallerDir + "/" + file + "/arianeaddondesc.json")
                            shutil.rmtree(tmpTestDir)
                            os.chdir(pwd)
                            return True
                        except FileNotFoundError:
                            shutil.rmtree(tmpTestDir)
                            os.chdir(pwd)
                            return "this Ariane addon package has a bad descriptor !"
                shutil.rmtree(tmpTestDir)
                os.chdir(pwd)
                return "this Ariane addon package doesn't have any descriptor ! "

            else:
                shutil.rmtree(tmpTestDir)
                os.chdir(pwd)
                return "this zip file doesn't have installer ! "

        else:
            return "provided path doesn't exists or is not a valid zip file ! "

    def getInstalledAddonDescription(self, addonName, addonVersion):
        for file in os.listdir(self.virgoHomePath + "/ariane/installer/addons"):
            if os.path.isdir(self.virgoHomePath + "/ariane/installer/addons/" + file) and os.path.exists(self.virgoHomePath + "/ariane/installer/addons/" + file + "/arianeaddondesc.json"):
                description = addonDesc(self.virgoHomePath + "/ariane/installer/addons/" + file + "/arianeaddondesc.json")
                if description.id == addonName and description.version == addonVersion:
                    return description
        return None

    @staticmethod
    def getInstalledAddonsDescription(virgoHomePath):
        descriptions = []
        for file in os.listdir(virgoHomePath + "/ariane/installer/addons"):
            if os.path.isdir(virgoHomePath + "/ariane/installer/addons/" + file) and os.path.exists(virgoHomePath + "/ariane/installer/addons/" + file + "/arianeaddondesc.json"):
                descriptions.append(addonDesc(virgoHomePath + "/ariane/installer/addons/" + file + "/arianeaddondesc.json"))
        return descriptions

    def installAddonPackage(self, addonPackagePath):
        ret = self.checkAddonPackage(addonPackagePath)
        if ret is True:
            pwd = os.getcwd()
            os.chdir(self.virgoHomePath)
            addonZip = zipfile.ZipFile(addonPackagePath)
            addonZip.extractall()
            os.chdir(pwd)
            print("\n%-- Provided Ariane addon package (" + addonPackagePath + ") has been installed successfully !")
        else:
            print("\n%-- Provided Ariane addon package (" + addonPackagePath + ") has not been installed as it is NOT valid ! Reason : " + ret)

    def uninstallAddonPackage(self, addonName, addonVersion):
        description = self.getInstalledAddonDescription(addonName, addonVersion)
        if description is not None:
            # remove jar and plan in ariane-plugins repository
            for file in os.listdir(self.virgoHomePath + "/repository/ariane-plugins"):
                print(addonVersion)
                if addonVersion == "master.SNAPSHOT":
                    if fnmatch.fnmatch(file, "*." + addonName + "*SNAPSHOT.*"):
                        os.remove(self.virgoHomePath + "/repository/ariane-plugins/" + file)
                else:
                    if fnmatch.fnmatch(file, "*." + addonName + ".*." + addonVersion + ".*"):
                        os.remove(self.virgoHomePath + "/repository/ariane-plugins/" + file)

            # remove configuration and template files
            for environment in description.environmentItems:
                if environment.sqlScriptFP is not None and os.path.exists(environment.getDirectorySqlScriptFP()):
                    shutil.rmtree(environment.getDirectorySqlScriptFP())

                elif environment.templateFP is not None and os.path.exists(environment.getDirectoryTemplateFP()):
                    shutil.rmtree(environment.getDirectoryTemplateFP())

                    if environment.defaultValuesFP is not None and os.path.exists(environment.getDirectoryDefaultValuesFP()):
                        shutil.rmtree(environment.getDirectoryDefaultValuesFP())

                    if os.path.exists(environment.targetConf):
                        os.remove(environment.targetConf)
                        dirTargetConf = environment.getDirectoryTargetConfFP()
                        if dirTargetConf != self.virgoHomePath + "/repository/ariane-plugins" and len(os.listdir(dirTargetConf)) == 0:
                            parentDir = os.path.abspath(os.path.join(dirTargetConf, os.pardir))
                            shutil.rmtree(dirTargetConf)
                            # from there remove empty parent dir
                            while len(os.listdir(parentDir)) == 0:
                                parentDir = os.path.abspath(os.path.join(parentDir, os.pardir))
                                shutil.rmtree(parentDir)

            # finally remove addon installer module
            shutil.rmtree(self.virgoHomePath + "/ariane/installer/" + description.hookPackage.replace(".", "/"))

            print("\n%-- Provided Ariane addon (" + addonName + "-" + addonVersion + ") has been successfully uninstalled !")
        else:
            print("\n%-- Provided Ariane addon (" + addonName + "-" + addonVersion + ") is not installed !")

    def listInstalledAddonPackages(self):
        addonCount = 0
        for file in os.listdir(self.virgoHomePath + "/ariane/installer/addons"):
            if os.path.isdir(self.virgoHomePath + "/ariane/installer/addons/" + file) and os.path.exists(self.virgoHomePath + "/ariane/installer/addons/" + file + "/arianeaddondesc.json"):
                if addonCount == 0:
                    print("\n\tInstalled Ariane addon(s) in " + self.virgoHomePath + " :\n")
                    print('\t{:30} {:30} {:30}'.format("Ariane addon name", "Ariane addon version", "Ariane addon type"))
                    print('\t{:30} {:30} {:30}'.format("-----------------", "--------------------", "-----------------"))
                addonCount += 1
                description = addonDesc(self.virgoHomePath + "/ariane/installer/addons/" + file + "/arianeaddondesc.json")
                print('\t{:30} {:30} {:30}'.format(description.id, description.version, description.type))

        if addonCount == 0:
            print("\n\t There is no installed ariane addon in " + self.virgoHomePath + " !")


class addonProcessor:

    def __init__(self, virgoHomePath, directoryDBConfig, idmDBConfig, silent):
        self.virgoHomePath = virgoHomePath
        self.directoryDBConfig = directoryDBConfig
        self.idmDBConfig = idmDBConfig
        self.silent = silent

    def getDeployCommandsFiles(self):
        list = []
        for description in addonInstaller.getInstalledAddonsDescription(self.virgoHomePath):
            for item in description.environmentItems:
                if item.deployCmdFP is not None:
                    list.append(item.deployCmdFP)
        return list

    def process(self):
        for description in addonInstaller.getInstalledAddonsDescription(self.virgoHomePath):
            imported = getattr(__import__(description.hookPackage + "." + description.hookModule, fromlist=[description.hookClass]), description.hookClass)
            imported(self.virgoHomePath, self.directoryDBConfig, self.idmDBConfig, self.silent).process()
        return self
