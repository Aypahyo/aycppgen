import os
import unittest
from unittest.mock import Mock

from aycppgen_core.generator import Generator

class TestFileSystem(unittest.TestCase):
    __uut : Generator = None

    def setUp(self) -> None:
        self.__filesytem = Mock()
        self.__uut = Generator(self.__filesytem)
        return super().setUp()
    
    def test_asdf(self):
        self.assertFalse(False)
