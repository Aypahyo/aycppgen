from genericpath import exists, isdir, isfile
from logging import Logger
import os
import unittest
from unittest.mock import Mock

from aycppgen_core.wrapfilesystem import LinuxFileSystem

class TestFileSystem(unittest.TestCase):
    __uut : LinuxFileSystem = None
    __logger : Logger = None

    def setUp(self) -> None:
        self.__testbasepath = "tests/test_wrapfilesystem_data"
        os.system(f'mkdir -p {self.__testbasepath}')
        self.__logger = Mock()
        self.__logger.handlers = ["fake"]
        self.__uut = LinuxFileSystem(logger=self.__logger)
        return super().setUp()

    def tearDown(self) -> None:
        if "tests" in self.__testbasepath:
            os.system(f'rm -rf {self.__testbasepath}')
        return super().tearDown()

    def test_make_folders(self):
        targets = [
            f'{self.__testbasepath}/folder/subfolder1',
            f'{self.__testbasepath}/folder/subfolder2',
            f'{self.__testbasepath}/folder/subfolder2_x2',
            f'{self.__testbasepath}/folder/subfolder2_x2/3',
        ]
        self.assertFalse(any([ exists(f) for f in targets]), "setup invalid target folders can not exist")
        success = self.__uut.create_folders(targets)
        self.assertTrue(success)
        self.assertTrue(all([ exists(f) for f in targets]), "target folders were not created")
        self.assertEqual(self.__logger.info.call_count, len(targets), 'not all executions were logged')

    def test_make_folders_failing(self):
        targets = [
            #it is insanely hard to create an invalid path
            f'',
        ]
        success = self.__uut.create_folders(targets)
        self.assertFalse(success)
        self.assertFalse(any([ exists(f) for f in targets]), "creating folders should be impossible")
        self.__logger.error.assert_called_once()

    def test_get_project_template_root(self):
        expected_end = "aycppgen_core/templates/project"
        tempalte_folder = self.__uut.get_project_template_root()
        self.assertTrue(tempalte_folder.endswith(expected_end), f'{tempalte_folder} does not end in {expected_end}')

    def test_glob_project_template_root(self):
        targets = self.__uut.glob_project_template_root()
        self.assertTrue(all([ exists(f) for f in targets]), 'all exists')
        self.assertTrue(any([ isfile(f) for f in targets]), 'any isfile')
        self.assertTrue(any([ isdir(f) for f in targets]), 'any isdir')
        self.assertTrue(any([ f.endswith("CMakeLists.txt") for f in targets]), 'any endswith("CMakeLists.txt")')
        self.assertTrue(any([ f.endswith("main.cpp") for f in targets]), 'any endswith("main.cpp")')

    def test_load_all_templates(self):
        entries = self.__uut.load_all_templates()
        self.assertTrue(all([ exists(e.name) for e in entries]), 'all exists')
        self.assertTrue(any([ isfile(f.name) for f in entries]), 'any isfile')
        self.assertTrue(any([ isdir(d.name) for d in entries]), 'any isdir')

        self.assertTrue(all([ e.name == f'{e.baseDir}/{e.relative}' for e in entries]), 'all exists')

        directores = [ d for d in entries if isdir(d.name)]
        self.assertTrue(all([ e.isDirectory and e.content is None for e in directores]), 'isdir and no content')

        files = [ f for f in entries if isfile(f.name)]
        self.assertTrue(all([ e.isFile and e.content is not None for e in files]), 'isfile and content')

    

