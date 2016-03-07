from py._path.local import LocalPath
import pytest
import os
import os.path

from junit_report_creator.collector import find_files

def create_subdirectories(path, amount, depth):
    path = str(path)
    for x in range(amount):
        p = LocalPath(path).join(str(x))
        p.mkdir()
        _f = p.join("testreport.xml")
        _f.write("")
        if not depth == 0:
            depth -= 1
            create_subdirectories(p, 1, depth)

@pytest.fixture
def testFilesSearchDirectory(tmpdir):
    for x in range(1):
        p = tmpdir.join(str(x))
        p.mkdir()
        create_subdirectories(p, 1, 100)
    return tmpdir


def test_find(testFilesSearchDirectory):
    _ = [f for f in find_files(testFilesSearchDirectory, "*.xml")]
    assert len(_) == 101
