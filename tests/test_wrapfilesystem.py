import os
import unittest

from aycppgen_core.wrapfilesystem import FileSystem

class TestFileSystem(unittest.TestCase):
    __uut : FileSystem = None

    def setUp(self) -> None:
        self.__uut = FileSystem()
        return super().setUp()
    
    def test_file_exists(self):
        self.assertFalse(self.__uut.fileExists(""))
