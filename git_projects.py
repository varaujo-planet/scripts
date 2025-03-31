import os
import subprocess
from pathlib import Path
from enum import IntEnum, Enum

class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
#################### Config parameters ####################
path_cpp = r'C:\Users\vitorjna\Desktop\branches\stable'
path_java = r'C:\Users\vitorjna\Desktop\Java-gerrit\gitrepos'

path_winmerge = r'C:\Program Files\WinMerge\WinMergeU.exe'
path_tortoise = r'c:\Program Files\TortoiseGit\bin\TortoiseGitProc.exe'

use_tortoise = True  # if False, will use git

class Projects(IntEnum):
    VF = 1
    PAX = 2
    ING = 3
    SDK = 4

def getRepos(project):
    match project:
        case Projects.VF:  return path_cpp, {"IntegraTEC_CppDK", "IntegraTEC_Core", "IntegraTEC_Verifone"}
        case Projects.PAX: return path_java, {"te-common-pax", "te-common-utils", "te-payment-core", "te-payment-controller-pax"}
        case Projects.ING: return path_cpp, {"IntegraTEC_CppDK", "IntegraTEC_Core", "IntegraTEC_Ingenico"}
        case Projects.SDK: return path_cpp, {"IntegraTEC_CppDK", "IntegraTE_ClientSDK_Cpp", "IntegraTE_ClientSDK_Java"}
        case _: return "", {}

#################### Config parameters end ####################

class Commands(IntEnum):
    PULL = 1
    PUSH = 2
    STATUS = 3
    CHECKOUT = 4
    LOG = 5
    POP = 6

class Tools(ExtendedEnum):
    TORT = "tortoise"
    GIT = "git"
    
def getCommandForTool(command, tool):
    match command:
        case Commands.PULL: return Commands.PULL.name.lower()
        case Commands.PUSH: return Commands.PUSH.name.lower()
        case Commands.STATUS:
            match tool:
                case Tools.TORT: return "repostatus"
                case _: return Commands.STATUS.name.lower()
        case Commands.CHECKOUT:
            match tool:
                case Tools.TORT: return "switch"
                case _: return Commands.CHECKOUT.name.lower()
        case Commands.POP:
            match tool:
                case Tools.GIT:  return "stash pop"
                case Tools.TORT: return "stashpop"
                case _: return Commands.CHECKOUT.name.lower()
        case Commands.LOG: return Commands.LOG.name.lower()
        case _: return ""


if __name__ == "__main__":

    project = input(f"Select a Project: {Projects._member_names_}: ").upper()
    reposLocation, repos = getRepos(Projects[project])
    print("Selected repos: " + str(repos))

    while True:
        command = input(f"Select a Command: {Commands._member_names_}: ").upper()
        if command == 'Q':
            break
            
        command = getCommandForTool(Commands[command], Tools.TORT)
        print("Selected command: " + command)

        for repo in repos:
            print(f'Running: "{path_tortoise}" /path:"{reposLocation}\\{repo}" /command:{command}')
            subprocess.run(f'"{path_tortoise}" /path:"{reposLocation}\\{repo}" /command:{command}', shell=True, stdout = subprocess.DEVNULL)
   

    os.system('pause')
