import os
import unittest
from unittest.mock import Mock
from aycppgen_core.FileSystemEntry import FileSystemEntry

from aycppgen_core.InterfaceManager import InterfaceManager, InterfaceSpecification
from aycppgen_core.wrapfilesystem import FileSystem
from aycppgen_core.linuxfilesystem import LinuxFileSystem

class TestInterfaceManager(unittest.TestCase):
    __uut : InterfaceManager = None
    __filesytem : FileSystem

    def setUp(self) -> None:
        self.__testbasepath = "tests/test_interfacemanager_data"
        os.system(f'mkdir -p {self.__testbasepath}')
        self.__filesytem_actual : FileSystem = LinuxFileSystem()
        self.__filesytem = Mock()
        self.__uut = InterfaceManager(self.__filesytem)
        return super().setUp()

    def test_rework_template(self):
        expected :FileSystemEntry = self.__filesytem_actual.load_file(f'{self.__testbasepath}/IAppliedInterfaceName.hpp')
        self.assertIsNotNone(expected.GetContent(), "setup invalid")
        
        input : FileSystemEntry = self.__filesytem_actual.load_file("aycppgen_core/templates/interface/template_interface_name.hpp")

        spec = InterfaceSpecification(
            target_folder = self.__testbasepath,
            template_namespace_name='ay::foo::bar',
            template_interface_name='IAppliedInterfaceName',
            template_methods=[ 'void a_run()', 'void c_run()', 'int b_run()']
            )

        actual = self.__uut.apply(spec, input)
        

        self.maxDiff = None
        self.assertEqual(expected.Preview(), actual.Preview())
