
from genericpath import isdir, isfile
from logging import Logger, getLogger
import os
from pathlib import Path

from aycppgen_core.generator import ContentFileOrDirectory, FileSystem

class LinuxFileSystem(FileSystem):
    def __init__(self, logger : Logger = None) -> None:
        self.__logger :Logger = logger if logger is not None else getLogger()
        super().__init__()

    def create_folders(self, folders : 'list[str]') -> bool:
        for folder in folders:
            command = f'mkdir -p "{folder}" '
            code = os.system(command)
            if code == 0:
                self.__logger.info(f'{code} {command}')
            else: 
                self.__logger.error(f'{code} {command}')
                return False
        return True

    def get_project_template_root(self) -> str:
        mydirectory = Path(__file__).resolve().parent
        project_template_root = f'{mydirectory}/project_template'

        while(mydirectory is not None):
            project_template_root = f'{mydirectory}/project_template'
            if isdir(project_template_root):
                return project_template_root
            self.__logger.debug(f'templates not found "{project_template_root}"')
            mydirectory = mydirectory.parent
        self.__logger.error(f'project_template not found')
        raise FileNotFoundError(f'project_template not found')

    def glob_project_template_root(self) -> 'list[str]':
        glob = Path(self.get_project_template_root()).glob("**/*")
        return list([str(g) for g in glob])

    def makeContentFileOrDirectory(self, name : str, baseDir : str) -> ContentFileOrDirectory:
        ret = ContentFileOrDirectory()
        ret.name = name
        ret.baseDir = baseDir
        ret.relative = name.replace(f'{baseDir}/', "")
        if isdir(name):
            ret.isDirectory = True
            ret.isFile = False
            ret.content = None
        elif isfile(name):
            ret.isDirectory = False
            ret.isFile = True
            with open(ret.name) as file:
                ret.content = file.read()
        else:
            raise FileExistsError(f'this factory assumes "{name}" is either a file or a directory')
        return ret

    def load_all_templates(self) -> 'list[ContentFileOrDirectory]':
        root = self.get_project_template_root()
        names = self.glob_project_template_root()
        return list([ self.makeContentFileOrDirectory(n, root) for n in names ])

    def write_files(self, files: 'list[ContentFileOrDirectory]') -> None:
        for templ in list([ t for t in files if t.isFile]):
            with open(f'{templ.name}', 'w+') as file:
                file.write(templ.content)
