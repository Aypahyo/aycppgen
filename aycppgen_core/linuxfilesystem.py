
from genericpath import isdir, isfile
from logging import Logger
import os
from pathlib import Path
from traceback import extract_tb
from aycppgen_core.FileSystemEntry import FileSystemEntry

from aycppgen_core.wrapfilesystem import FileSystem
from aycppgen_core.logginghelper import logginghelper_getOrDefault


class LinuxFileSystem(FileSystem):
    def __init__(self, logger : Logger = None) -> None:
        self.__logger :Logger = logginghelper_getOrDefault("LinuxFileSystem", logger)
        super().__init__()

    def create_folders(self, folders : 'list[str]') -> bool:
        for folder in folders:
            #todo replace os.system call so errors can be redirected to logging
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
        project_template_root = f'{mydirectory}/templates/project'

        while(mydirectory is not None):
            project_template_root = f'{mydirectory}/templates/project'
            if isdir(project_template_root):
                return project_template_root
            self.__logger.debug(f'templates not found "{project_template_root}"')
            mydirectory = mydirectory.parent
        self.__logger.error(f'project_template not found')
        raise FileNotFoundError(f'project_template not found')

    def glob_project_template_root(self) -> 'list[str]':
        glob = Path(self.get_project_template_root()).glob("**/*")
        return list([str(g) for g in glob])

    def load_all_templates(self) -> 'list[FileSystemEntry]':
        root = self.get_project_template_root()
        names = self.glob_project_template_root()
        return list([ self.makeFileSystemEntry(n, root) for n in names ])

    def write_files(self, files: 'list[FileSystemEntry]') -> None:
        for templ in list([ t for t in files if t.IsFile()]):
            with open(f'{templ.GetName()}', 'w+') as file:
                file.write(templ.GetContent())

    def load_file(self, fullpath, baseDir = None) -> FileSystemEntry:
        if baseDir is None:
            baseDir = Path(fullpath).parent
        return self.makeFileSystemEntry(fullpath, baseDir)

    def makeFileSystemEntry(self, name : str, baseDir : str) -> FileSystemEntry:
        baseDir = baseDir
        relative = name.replace(f'{baseDir}/', "")
        if isdir(name):
            return FileSystemEntry.FromDirectoy(baseDir, relative)
        elif isfile(name):
            try:
                with open(name, "r", encoding="utf-8") as file:
                    content = file.read()
            except Exception as e:
                self.__logger.error(f'{name}')
                self.__logger.error(f'{type(e)}: {e}')
                self.__logger.error(f'{extract_tb(e.__traceback__)}'.replace(",", ",\n"))
                raise e

            return FileSystemEntry.FromFile(baseDir, relative, content)
        else:
            raise FileExistsError(f'this factory assumes "{name}" is either a file or a directory')
