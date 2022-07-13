import json
import jsonpickle


class FileSystemEntry:
    __baseDir : str
    __relative : str
    __content : str

    def __init__(self) -> None:
        self.__baseDir = ""
        self.__relative = ""
        self.__content = None

    def SetBaseDir(self, baseDir : str) -> None:
        self.__baseDir = baseDir

    def ReplaceRelative(self, old: str, new : str) -> None:
        self.__relative = self.__relative.replace(old, new)

    def ReplaceContent(self, old: str, new : str) -> None:
        if self.__content is None:
            raise ValueError(f'file "{self.GetName()}" has content set to None')
        self.__content = self.__content.replace(old, new)

    def SetPath(self, base : str, relative : str) -> None:
        self.__baseDir = base
        self.__relative = relative

    def SetAsFile(self, content  :str) -> None:
        self.__content = "" if content is None else content

    def SetAsDirectory(self) -> None:
        self.__content = None

    def IsFile(self) -> bool:
        return self.__content != None

    def IsDirectory(self) -> bool:
        return self.__content == None

    def GetName(self) -> str:
        return f'{self.__baseDir}/{self.__relative}'

    def GetRelative(self) -> str:
        return self.__relative

    def GetBase(self) -> str:
        return self.__baseDir

    def GetContent(self) -> str:
        return self.__content

    def Preview(self) -> str:
        return  f'''file:
{self.GetName()}
content:
{self.GetContent()}'''

    def __eq__(self, __o: object) -> bool:
        return self.__repr__() == __o.__repr__()

    def __repr__(self) -> str:
        return json.dumps(json.loads(jsonpickle.dumps(self)), indent=1)

    def __hash__(self) -> int:
        return 0

    def __str__(self) -> str:
        indicator = "F" if self.IsFile() else "D"
        return f'{indicator} {self.GetRelative()}'

    @classmethod
    def FromCopy(cls, other = None) -> 'FileSystemEntry':
        if not isinstance(other, FileSystemEntry):
            TypeError(f'expected {FileSystemEntry} but was {type(other)}')
        created = FileSystemEntry()
        created.SetPath(other.GetBase(), other.GetRelative())
        if other.IsFile():
            created.SetAsFile(other.GetContent())
        return created

    @classmethod
    def FromDirectoy(cls, baseDir : str , relative : str) -> 'FileSystemEntry':
        created = FileSystemEntry()
        created.SetPath(baseDir, relative)
        return created

    @classmethod
    def FromFile(cls, baseDir : str , relative : str, content : str) -> 'FileSystemEntry':
        created = FileSystemEntry()
        created.SetPath(baseDir, relative)
        created.SetAsFile(content)
        return created

    @classmethod
    def FromJsonPickle(cls, jsonpickle_str : str) -> 'FileSystemEntry':
        return jsonpickle.loads(jsonpickle_str)