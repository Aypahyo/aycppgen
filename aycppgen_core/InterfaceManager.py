from dataclasses import dataclass
from pathlib import Path
import re
from aycppgen_core.FileSystemEntry import FileSystemEntry
from aycppgen_core.wrapfilesystem import FileSystem

@dataclass
class InterfaceSpecification():
    target_folder : str
    template_namespace_name : str
    template_interface_name : str
    template_methods : list
    def template_ifdef_name(self) -> str:
        return re.sub("[^A-Za-z0-9_]", "_", f'{self.template_namespace_name.replace("::", ":")}_{self.template_interface_name}_').upper()

class InterfaceManager():
    def __init__(self, file_manager :FileSystem) -> None:
        self.__filesytem = file_manager

    def apply(self, spec : InterfaceSpecification, input: FileSystemEntry = None) -> FileSystemEntry:
        if input is None:
            input : FileSystemEntry = self.__filesytem.load_file("aycppgen_core/templates/interface/template_interface_name.hpp")
        if input.IsDirectory():
            raise ValueError("Interface manager apply does not work on directories")
        rv = FileSystemEntry.FromCopy(input)
        rv.SetBaseDir(spec.target_folder)
        rv.ReplaceRelative("template_interface_name", spec.template_interface_name)

        rv.ReplaceContent("template_ifdef_name", spec.template_ifdef_name())
        rv.ReplaceContent("template_namespace_name", spec.template_namespace_name)
        rv.ReplaceContent("template_interface_name", spec.template_interface_name)

        def getname( definition : str):
            definition_pattern = r"^\w+ (?P<NAME>\w+)\(.+$"
            match = re.search(definition_pattern, definition)
            if match is None:
                raise ValueError(f'"{definition}" does not conform to pattern r"{definition_pattern}"')
            name = match.group("NAME")
            return name
        methods = spec.template_methods.copy()
        methods.sort(key=getname)
        rv.ReplaceContent("template_methods", "\n".join(list([f'  virtual {m} = 0;' for m in methods])))
        return rv

    def writeInterface(self, target : FileSystemEntry):
        self.__filesytem.write_files([target])

    def find_namespace_name(self, selected : list[FileSystemEntry]) -> str:
        if selected is not None and len(selected) == 1 and selected[0].IsDirectory():
            file_names = [ str(g) for g in Path(selected[0].GetName()).glob("*.hpp")]
            for f_name in file_names:
                f_loaded = self.__filesytem.load_file(f_name)
                match = re.search(r"namespace\s*(?P<NAMESPACE>.+?)\s*\{", f_loaded.GetContent(), re.MULTILINE)
                if match is not None:
                    return match.group("NAMESPACE")
            return "namespace"
        else:
            return "namespace"