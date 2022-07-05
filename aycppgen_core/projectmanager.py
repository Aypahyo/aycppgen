from genericpath import isdir
from pathlib import Path

from aycppgen_core.config import Config
from aycppgen_core.generator import ProjectSpec, Generator
from aycppgen_core.wrapfilesystem import LinuxFileSystem


class ProjectManager:
    def __init__(self, config : Config) -> None:
        self.__config = config
        self.__project_explorer_base = ""
        self.__project_explorer_base_contents = []

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
            content = [str(g).replace(f'{self.get_project_explorer_base()}/', "") for g in Path(self.get_project_explorer_base()).glob("**/*") if "/." not in str(g) and self.get_project_explorer_base() != str(g) ]
            content.sort()
        else:
            content = []
        
        if self.__project_explorer_base_contents == content:
            return False
        else:
            self.__project_explorer_base_contents = content
            return True

    def get_project_explorer_base_content(self) -> bool:
        if isinstance(self.__project_explorer_base_contents, list):
            return self.__project_explorer_base_contents
        else:
            return []

    def get_project_explorer_base(self) -> str:
        if isinstance(self.__project_explorer_base, str):
            return self.__project_explorer_base
        return ""

    def can_create_project(self) -> bool:
        dir = isdir(self.get_project_explorer_base())
        dir_mostly_empty = len(self.get_project_explorer_base_content()) < 5
        return dir & dir_mostly_empty

    def create_project(self) -> None:
        spec = ProjectSpec("genproject")
        gen = Generator(LinuxFileSystem())
        gen.CreateProject(spec, self.get_project_explorer_base())