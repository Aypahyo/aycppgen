import os
from aycppgen_core.FileSystemEntry import FileSystemEntry

from aycppgen_core.wrapfilesystem import FileSystem

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
            if templ.IsFile():
                templ : FileSystemEntry
                templ.ReplaceContent("template_project_name", spec.name)
        dirs = list(f'{t.name}' for t in templates if t.IsDirectory())
        self.__filesysystem.create_folders(dirs)
        files = list([ t for t in templates if t.IsFile()])
        self.__filesysystem.write_files(files)
