import unittest
from aycppgen_core.FileSystemEntry import FileSystemEntry

class TestFileSystemEntry(unittest.TestCase):

    def setUp(self) -> None:
        self.__sample = FileSystemEntry.FromJsonPickle(
        '''{
        "py/object": "aycppgen_core.FileSystemEntry.FileSystemEntry",
        "__baseDir": "base/dir",
        "__relative": "sub/path",
        "__content": null
        }
        '''
        )
        return super().setUp()

    def test_ctor_copy_dir(self):
        original : FileSystemEntry = self.__sample
        original.SetAsDirectory()
        copy : FileSystemEntry = FileSystemEntry.FromCopy(original)
        self.assertEqual(original.__repr__(), copy.__repr__())

    def test_ctor_copy_file(self):
        original : FileSystemEntry = self.__sample
        original.SetAsFile("c")
        copy : FileSystemEntry = FileSystemEntry.FromCopy(original)
        self.assertEqual(original.__repr__(), copy.__repr__())

    def test_ctor_directory(self):
        expected: FileSystemEntry = self.__sample
        actual : FileSystemEntry = FileSystemEntry.FromDirectoy(expected.GetBase(), expected.GetRelative())
        self.assertEqual(expected, actual)

    def test_ctor_file(self):
        expected: FileSystemEntry = self.__sample
        expected.SetPath("base/dir", "sub/path/file.txt")
        expected.SetAsFile("content")
        actual : FileSystemEntry = FileSystemEntry.FromFile("base/dir", "sub/path/file.txt", "content")
        self.assertEqual(expected, actual)

    def test_set_baseDir(self):
        expected: FileSystemEntry = self.__sample
        expected.SetPath("replaced", "sub/path")
        actual : FileSystemEntry = FileSystemEntry.FromDirectoy("base/dir", "sub/path")
        actual.SetBaseDir("replaced")
        self.assertEqual(expected, actual)

    def test_replace_relative(self):
        expected: FileSystemEntry = self.__sample
        expected.SetPath("base/dir", "sub/replaced")
        actual : FileSystemEntry = FileSystemEntry.FromDirectoy("base/dir", "sub/template")
        actual.ReplaceRelative("template","replaced")
        self.assertEqual(expected, actual)

    def test_replace_content(self):
        expected: FileSystemEntry = self.__sample
        expected.SetAsFile("this replaced was")
        actual : FileSystemEntry = FileSystemEntry.FromFile("base/dir", "sub/path", "this template was")
        actual.ReplaceContent("template","replaced")
        self.assertEqual(expected, actual)

    def test_get_name(self):
        expected : str = "base/dir/sub/folder"
        actual : str = FileSystemEntry.FromDirectoy("base/dir", "sub/folder").GetName()
        self.assertEqual(expected, actual)

    def test_get_relative(self):
        expected : str = "sub/folder"
        actual : str = FileSystemEntry.FromDirectoy("base/dir", "sub/folder").GetRelative()
        self.assertEqual(expected, actual)

    def test_get_relative(self):
        expected : str = "base/dir"
        actual : str = FileSystemEntry.FromDirectoy("base/dir", "sub/folder").GetBase()
        self.assertEqual(expected, actual)

    def test_get_content(self):
        self.assertEqual(None, FileSystemEntry.FromDirectoy("base/dir", "sub/folder").GetContent())
        self.assertEqual("content", FileSystemEntry.FromFile("base/dir", "sub/folder", "content").GetContent())

    def test_set_path(self):
        expected : str = "b/r"
        uut : FileSystemEntry = FileSystemEntry.FromDirectoy("base/dir", "sub/folder")
        uut.SetPath("b", "r")
        actual : str = uut.GetName()
        self.assertEqual(expected, actual)

    def test_set_as_file(self):
        expected : str = FileSystemEntry.FromFile("base/dir", "sub/folder", "content")
        actual : str = FileSystemEntry.FromDirectoy("base/dir", "sub/folder")
        actual.SetAsFile("content")
        self.assertEqual(expected, actual)

    def test_set_as_file_missing_content(self):
        expected : str = FileSystemEntry.FromFile("base/dir", "sub/folder", "")
        actual : str = FileSystemEntry.FromDirectoy("base/dir", "sub/folder")
        actual.SetAsFile(None)
        self.assertEqual(expected, actual)
        self.assertTrue(actual.IsFile())

    def test_set_as_directory(self):
        expected : str = FileSystemEntry.FromDirectoy("base/dir", "sub/folder")
        actual : str = FileSystemEntry.FromFile("base/dir", "sub/folder", "content")
        actual.SetAsDirectory()
        self.assertEqual(expected, actual)
        self.assertTrue(actual.IsDirectory())

    def test_preview(self):
        expected =  f'''file:
base/dir/sub/file.txt
content:
line one
line two'''
        actual : str = FileSystemEntry.FromFile("base/dir", "sub/file.txt", "line one\nline two").Preview()
        self.assertEqual(expected, actual)

    def test_str(self):
        self.assertEqual("D sub/myfolder", f'{FileSystemEntry.FromDirectoy("base/dir", "sub/myfolder")}')
        self.assertEqual("F sub/file.txt", f'{FileSystemEntry.FromFile("base/dir", "sub/file.txt", "")}')