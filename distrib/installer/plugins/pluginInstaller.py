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
from tools.PluginDesc import pluginDesc

__author__ = 'mffrench'


class pluginInstaller:

    def __init__(self, virgoHomePath):
        self.virgoHomePath = virgoHomePath

    def checkPluginPackage(self, pluginPackagePath):
        if os.path.exists(pluginPackagePath) and zipfile.is_zipfile(pluginPackagePath):
            tmpTestDir = tempfile.mkdtemp()
            pwd = os.getcwd()
            os.chdir(tmpTestDir)
            pluginZip = zipfile.ZipFile(pluginPackagePath)
            pluginZip.extractall()

            pluginInstallerDir = tmpTestDir + "/ariane/installer/plugins"
            if os.path.exists(pluginInstallerDir) and os.path.isdir(pluginInstallerDir):
                for file in os.listdir(pluginInstallerDir):
                    if os.path.isdir(pluginInstallerDir + "/" + file) and os.path.exists(pluginInstallerDir + "/" + file + "/arianeplugindesc.json"):
                        try:
                            pluginDesc(pluginInstallerDir + "/" + file + "/arianeplugindesc.json")
                            shutil.rmtree(tmpTestDir)
                            os.chdir(pwd)
                            return True
                        except FileNotFoundError:
                            shutil.rmtree(tmpTestDir)
                            os.chdir(pwd)
                            return "this Ariane plugin package has a bad descriptor !"
                shutil.rmtree(tmpTestDir)
                os.chdir(pwd)
                return "this Ariane plugin package doesn't have any descriptor ! "

            else:
                shutil.rmtree(tmpTestDir)
                os.chdir(pwd)
                return "this zip file doesn't have installer ! "

        else:
            return "provided path doesn't exists or is not a valid zip file ! "

    def getInstalledPluginDescription(self, pluginName, pluginVersion):
        for file in os.listdir(self.virgoHomePath + "/ariane/installer/plugins"):
            if os.path.isdir(self.virgoHomePath + "/ariane/installer/plugins/" + file) and os.path.exists(self.virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"):
                description = pluginDesc(self.virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json")
                if description.id == pluginName and description.version == pluginVersion:
                    return description
        return None

    @staticmethod
    def getInstalledPluginsDescription(virgoHomePath):
        descriptions = []
        for file in os.listdir(virgoHomePath + "/ariane/installer/plugins"):
            if os.path.isdir(virgoHomePath + "/ariane/installer/plugins/" + file) and os.path.exists(virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"):
                descriptions.append(pluginDesc(virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"))
        return descriptions

    def installPluginPackage(self, pluginPackagePath):
        ret = self.checkPluginPackage(pluginPackagePath)
        if ret is True:
            pwd = os.getcwd()
            os.chdir(self.virgoHomePath)
            pluginZip = zipfile.ZipFile(pluginPackagePath)
            pluginZip.extractall()
            os.chdir(pwd)
            print("\n%-- Provided Ariane plugin package (" + pluginPackagePath + ") has been installed successfully !")
        else:
            print("\n%-- Provided Ariane plugin package (" + pluginPackagePath + ") has not been installed as it is NOT valid ! Reason : " + ret)

    def uninstallPluginPackage(self, pluginName, pluginVersion):
        description = self.getInstalledPluginDescription(pluginName, pluginVersion)
        if description is not None:
            # remove jar and plan in ariane-plugins repository
            for file in os.listdir(self.virgoHomePath + "/repository/ariane-plugins"):
                if pluginVersion == "master.SNAPSHOT":
                    if fnmatch.fnmatch(file, "*." + pluginName + "*SNAPSHOT.*"):
                        os.remove(self.virgoHomePath + "/repository/ariane-plugins/" + file)
                else:
                    if fnmatch.fnmatch(file, "*." + pluginName + ".*." + pluginVersion + ".*"):
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

            print("\n%-- Provided Ariane plugin (" + pluginName + "-" + pluginVersion + ") has been successfully uninstalled !")
        else:
            print("\n%-- Provided Ariane plugin (" + pluginName + "-" + pluginVersion + ") is not installed !")

    def listInstalledPluginPackages(self):
        addonCount = 0
        for file in os.listdir(self.virgoHomePath + "/ariane/installer/plugins"):
            if os.path.isdir(self.virgoHomePath + "/ariane/installer/plugins/" + file) and os.path.exists(self.virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"):
                if addonCount == 0:
                    print("\n\tInstalled Ariane plugin(s) in " + self.virgoHomePath + " :\n")
                    print('\t{:40} {:30} {:30}'.format("Ariane plugin name", "Ariane plugin version", "Ariane plugin type"))
                    print('\t{:40} {:30} {:30}'.format("------------------", "---------------------", "------------------"))
                addonCount += 1
                description = pluginDesc(self.virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json")
                print('\t{:40} {:30} {:30}'.format(description.id, description.version, description.type))

        if addonCount == 0:
            print("\n\t There is no installed ariane plugin in " + self.virgoHomePath + " !")


class pluginProcessor:

    def __init__(self, virgoHomePath, directoryDBConfig, idmDBConfig, silent):
        self.virgoHomePath = virgoHomePath
        self.directoryDBConfig = directoryDBConfig
        self.idmDBConfig = idmDBConfig
        self.silent = silent

    def getDeployCommandsFiles(self):
        list = []
        for description in pluginInstaller.getInstalledPluginsDescription(self.virgoHomePath):
            for item in description.environmentItems:
                if item.deployCmdFP is not None:
                    list.append(item.deployCmdFP)
        return list

    def process(self):
        for description in pluginInstaller.getInstalledPluginsDescription(self.virgoHomePath):
            imported = getattr(__import__(description.hookPackage + "." + description.hookModule, fromlist=[description.hookClass]), description.hookClass)
            imported(self.virgoHomePath, self.directoryDBConfig, self.idmDBConfig, self.silent).process()
        return self
