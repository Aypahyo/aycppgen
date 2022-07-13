from genericpath import isdir
from pathlib import Path
from aycppgen_core.FileSystemEntry import FileSystemEntry

from aycppgen_core.config import Config
from aycppgen_core.generator import ProjectSpec, Generator
from aycppgen_core.linuxfilesystem import LinuxFileSystem


class ProjectManager:
    def __init__(self, config : Config) -> None:
        self.__config = config
        self.__project_explorer_base = ""
        self.__project_explorer_base_contents = []
        self.__project_explorer_base_selected = []
        self.__fileSystem = LinuxFileSystem() # todo pull service one level up

    def try_update_project_explorer_base(self, project_explorer_base : str ) -> bool:
        if not isinstance(project_explorer_base, str):
            project_explorer_base = ""
        if self.__project_explorer_base != project_explorer_base:
            self.__project_explorer_base = project_explorer_base
            return True
        else:
            return False

    def try_update_project_explorer_base_content(self) -> bool:
        if isdir(self.get_project_explorer_base()):
            b = self.get_project_explorer_base()
            content = list([self.__fileSystem.load_file(str(g), b) for g in Path(b).glob("**/*") if "/." not in str(g) and b != str(g) ])
            #content : list[FileSystemEntry]
            #content.sort(key=FileSystemEntry.GetRelative())
        else:
            content = []
        
        if self.__project_explorer_base_contents == content:
            return False
        else:
            self.__project_explorer_base_contents = content
            return True

    def get_project_explorer_base_content(self) -> 'list[FileSystemEntry]':
        if isinstance(self.__project_explorer_base_contents, list):
            return self.__project_explorer_base_contents
        else:
            return []

    def get_project_explorer_base(self) -> str:
        if isinstance(self.__project_explorer_base, str):
            return self.__project_explorer_base
        return ""

    def set_project_explorer_base_selected(self, selected : 'list[FileSystemEntry]') -> None:
        self.__project_explorer_base_selected = selected

    def get_project_explorer_base_selected(self) -> None:
        return self.__project_explorer_base_selected

    def can_create_project(self, proj_name) -> bool:
        if(proj_name is None or proj_name == ""):
            return False
        proj_name
        dir = isdir(self.get_project_explorer_base())
        dir_mostly_empty = len(self.get_project_explorer_base_content()) < 5
        return dir & dir_mostly_empty

    def create_project(self, proj_name) -> None:
        spec = ProjectSpec(proj_name)
        gen = Generator(LinuxFileSystem())
        gen.CreateProject(spec, self.get_project_explorer_base())