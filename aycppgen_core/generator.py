from aycppgen_core.wrapfilesystem import FileSystem


ELEMENT_PROJECT = "project"
ELEMENT_INTERFACE = "interface"
ELEMENT_CLASS = "class"
ELEMENT_DTO = "dto"

COMMAND_CREATE = "create"

elements = [ELEMENT_PROJECT, ELEMENT_INTERFACE, ELEMENT_CLASS, ELEMENT_DTO]
commands = [COMMAND_CREATE]


class Generator:
    def __init__(self, filesystem : FileSystem) -> None:
        self.__filesysystem = filesystem
        