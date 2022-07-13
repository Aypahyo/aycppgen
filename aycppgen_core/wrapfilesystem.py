from aycppgen_core.FileSystemEntry import FileSystemEntry


class FileSystem:
    def load_file(self, fullpath, baseDir = None) -> FileSystemEntry:
        pass
    def load_all_templates(self, name) -> 'list[FileSystemEntry]':
        pass
    def create_folders(self, folders : 'list[str]') -> bool:
        pass
    def write_files(self, files: 'list[FileSystemEntry]') -> None:
        pass
