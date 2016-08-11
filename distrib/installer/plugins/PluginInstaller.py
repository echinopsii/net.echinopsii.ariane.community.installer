# Ariane plugin installer main
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
from tools.PluginDesc import PluginDesc

__author__ = 'mffrench'


class PluginInstaller:

    def __init__(self, virgo_home_path):
        self.virgoHomePath = virgo_home_path

    @staticmethod
    def check_plugin_package(plugin_package_path):
        if os.path.exists(plugin_package_path) and zipfile.is_zipfile(plugin_package_path):
            tmp_test_dir = tempfile.mkdtemp()
            pwd = os.getcwd()
            os.chdir(tmp_test_dir)
            plugin_zip = zipfile.ZipFile(plugin_package_path)
            plugin_zip.extractall()

            plugin_installer_dir = tmp_test_dir + "/ariane/installer/plugins"
            if os.path.exists(plugin_installer_dir) and os.path.isdir(plugin_installer_dir):
                for file in os.listdir(plugin_installer_dir):
                    if os.path.isdir(plugin_installer_dir + "/" + file) and os.path.exists(plugin_installer_dir + "/" +
                                                                                           file +
                                                                                           "/arianeplugindesc.json"):
                        try:
                            PluginDesc(plugin_installer_dir + "/" + file + "/arianeplugindesc.json")
                            shutil.rmtree(tmp_test_dir)
                            os.chdir(pwd)
                            return True
                        except FileNotFoundError:
                            shutil.rmtree(tmp_test_dir)
                            os.chdir(pwd)
                            return "this Ariane plugin package has a bad descriptor !"
                shutil.rmtree(tmp_test_dir)
                os.chdir(pwd)
                return "this Ariane plugin package doesn't have any descriptor ! "

            else:
                shutil.rmtree(tmp_test_dir)
                os.chdir(pwd)
                return "this zip file doesn't have installer ! "

        else:
            return "provided path doesn't exists or is not a valid zip file ! "

    def get_installed_plugin_description(self, plugin_name, plugin_version):
        for file in os.listdir(self.virgoHomePath + "/ariane/installer/plugins"):
            if os.path.isdir(self.virgoHomePath + "/ariane/installer/plugins/" + file) and \
                    os.path.exists(self.virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"):
                description = PluginDesc(self.virgoHomePath + "/ariane/installer/plugins/" + file +
                                         "/arianeplugindesc.json")
                if description.id == plugin_name and description.version == plugin_version:
                    return description
        return None

    @staticmethod
    def get_installed_plugins_description(virgo_home_path):
        descriptions = []
        for file in os.listdir(virgo_home_path + "/ariane/installer/plugins"):
            if os.path.isdir(virgo_home_path + "/ariane/installer/plugins/" + file) and \
                    os.path.exists(virgo_home_path + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"):
                descriptions.append(PluginDesc(virgo_home_path + "/ariane/installer/plugins/" + file +
                                               "/arianeplugindesc.json"))
        return descriptions

    def install_plugin_package(self, plugin_package_path):
        ret = self.check_plugin_package(plugin_package_path)
        if ret is True:
            pwd = os.getcwd()
            os.chdir(self.virgoHomePath)
            plugin_zip = zipfile.ZipFile(plugin_package_path)
            plugin_zip.extractall()
            os.chdir(pwd)
            print("\n%-- Provided Ariane plugin package (" + plugin_package_path +
                  ") has been installed successfully !")
        else:
            print("\n%-- Provided Ariane plugin package (" + plugin_package_path +
                  ") has not been installed as it is NOT valid ! Reason : " + ret)

    def uninstall_plugin_package(self, plugin_name, plugin_version):
        description = self.get_installed_plugin_description(plugin_name, plugin_version)
        if description is not None:
            # remove jar and plan in ariane-plugins repository
            for file in os.listdir(self.virgoHomePath + "/repository/ariane-plugins"):
                if plugin_version == "master.SNAPSHOT":
                    if fnmatch.fnmatch(file, "*." + plugin_name + "*SNAPSHOT.*"):
                        os.remove(self.virgoHomePath + "/repository/ariane-plugins/" + file)
                else:
                    if fnmatch.fnmatch(file, "*." + plugin_name + ".*." + plugin_version + ".*"):
                        os.remove(self.virgoHomePath + "/repository/ariane-plugins/" + file)

            # remove configuration and template files
            for environment in description.environmentItems:
                if environment.sqlScriptFP is not None and os.path.exists(environment.get_directory_sql_script_fp()):
                    shutil.rmtree(environment.get_directory_sql_script_fp())

                elif environment.templateFP is not None and os.path.exists(environment.get_directory_template_fp()):
                    shutil.rmtree(environment.get_directory_template_fp())

                    if environment.defaultValuesFP is not None and \
                            os.path.exists(environment.get_directory_default_values_fp()):
                        shutil.rmtree(environment.get_directory_default_values_fp())

                    if os.path.exists(environment.targetConf):
                        os.remove(environment.targetConf)
                        dir_target_conf = environment.get_directory_target_conf_fp()
                        if dir_target_conf != self.virgoHomePath + "/repository/ariane-plugins" and \
                                len(os.listdir(dir_target_conf)) == 0:
                            parent_dir = os.path.abspath(os.path.join(dir_target_conf, os.pardir))
                            shutil.rmtree(dir_target_conf)
                            # from there remove empty parent dir
                            while len(os.listdir(parent_dir)) == 0:
                                parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
                                shutil.rmtree(parent_dir)

            # finally remove addon installer module
            shutil.rmtree(self.virgoHomePath + "/ariane/installer/" + description.hookPackage.replace(".", "/"))

            print("\n%-- Provided Ariane plugin (" + plugin_name + "-" + plugin_version +
                  ") has been successfully uninstalled !")
        else:
            print("\n%-- Provided Ariane plugin (" + plugin_name + "-" + plugin_version + ") is not installed !")

    def list_installed_plugin_packages(self):
        addon_count = 0
        for file in os.listdir(self.virgoHomePath + "/ariane/installer/plugins"):
            if os.path.isdir(self.virgoHomePath + "/ariane/installer/plugins/" + file) and \
                    os.path.exists(self.virgoHomePath + "/ariane/installer/plugins/" + file + "/arianeplugindesc.json"):
                if addon_count == 0:
                    print("\n\tInstalled Ariane plugin(s) in " + self.virgoHomePath + " :\n")
                    print('\t{:40} {:30} {:30}'.format("Ariane plugin name", "Ariane plugin version",
                                                       "Ariane plugin type"))
                    print('\t{:40} {:30} {:30}'.format("------------------", "---------------------",
                                                       "------------------"))
                addon_count += 1
                description = PluginDesc(self.virgoHomePath + "/ariane/installer/plugins/" + file +
                                         "/arianeplugindesc.json")
                print('\t{:40} {:30} {:30}'.format(description.id, description.version, description.type))

        if addon_count == 0:
            print("\n\t There is no installed ariane plugin in " + self.virgoHomePath + " !")


class PluginProcessor:

    def __init__(self, home_path, dist_dep_type, directory_db_config, idm_db_config, silent):
        self.homePath = home_path
        self.dist_dep_type = dist_dep_type
        self.directoryDBConfig = directory_db_config
        self.idmDBConfig = idm_db_config
        self.silent = silent

    def get_deploy_commands_files(self):
        ret_list = []
        for description in PluginInstaller.get_installed_plugins_description(self.homePath):
            for item in description.environmentItems:
                if item.deployCmdFP is not None:
                    ret_list.append(item.deployCmdFP)
        return ret_list

    def process(self):
        for description in PluginInstaller.get_installed_plugins_description(self.homePath):
            imported = getattr(__import__(description.hookPackage + "." + description.hookModule,
                                          fromlist=[description.hookClass]), description.hookClass)
            imported(self.homePath, self.directoryDBConfig, self.idmDBConfig, self.silent).process()
        return self
