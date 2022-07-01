import os
from re import template


ELEMENT_PROJECT = "project"
ELEMENT_INTERFACE = "interface"
ELEMENT_CLASS = "class"
ELEMENT_DTO = "dto"

COMMAND_CREATE = "create"

elements = [ELEMENT_PROJECT, ELEMENT_INTERFACE, ELEMENT_CLASS, ELEMENT_DTO]
commands = [COMMAND_CREATE]

class ContentFileOrDirectory:
    name : str = ""
    baseDir : str = ""
    relative : str = ""
    content : str = ""
    isDirectory : bool = False
    isFile : bool = False

class FileSystem:
    def load_all_templates(self) -> 'list[ContentFileOrDirectory]':
        pass
    def create_folders(self, folders : 'list[str]') -> bool:
        pass
    def write_files(self, files: 'list[ContentFileOrDirectory]') -> None:
        pass

#todo test that project spec functions as intended with regard to folder initialisation
class ProjectSpec:
    name :str = None
    def __init__(self, name: str) -> None:
        self.name = name

class Generator:
    def __init__(self, filesystem : FileSystem) -> None:
        self.__filesysystem = filesystem

    def CreateProject(self, spec : ProjectSpec, base_dir = None ) -> None:
        if base_dir is None:
            base_dir = os.getcwd()
        templates = self.__filesysystem.load_all_templates()
        for templ in templates:
            templ.baseDir = base_dir
            templ.relative = templ.relative.replace("template_project_name", spec.name)
            templ.name= f'{templ.baseDir}/{templ.relative}'
            if templ.isFile:
                templ.content = templ.content.replace("template_project_name", spec.name)
        dirs = list(f'{t.name}' for t in templates if t.isDirectory)
        self.__filesysystem.create_folders(dirs)
        files = list([ t for t in templates if t.isFile])
        self.__filesysystem.write_files(files)
