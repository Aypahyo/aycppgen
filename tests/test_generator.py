import os
import unittest
from unittest.mock import MagicMock, Mock

from aycppgen_core.generator import FileSystem, Generator, ProjectSpec

class TestFileSystem(unittest.TestCase):
    __uut : Generator = None
    __filesytem : FileSystem

    def setUp(self) -> None:
        self.__testbasepath = "tests/test_generator_data"
        os.system(f'mkdir -p {self.__testbasepath}')
        self.__filesytem = Mock()
        self.__uut = Generator(self.__filesytem)
        return super().setUp()

    def tearDown(self) -> None:
        if "tests" in self.__testbasepath:
            os.system(f'rm -rf {self.__testbasepath}')
        return super().tearDown()

    def test_createProject_createsFolders(self):
        spec = ProjectSpec("AyTruffle")
        self.__filesytem.load_all_templates = MagicMock(return_value=list())
        self.__uut.CreateProject(spec, base_dir = self.__testbasepath)
        self.__filesytem.create_folders.assert_called_once()
