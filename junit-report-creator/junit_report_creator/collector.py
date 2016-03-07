import os
import fnmatch
import logging
import pathlib

log = logging.getLogger()



def find_files(directory, pattern):
    """Searching for pattern in specific directory.
    Returns an list with found files and directories according to
    given pattern.

    :param dirPathToSearch:
    :param pattern: No tilde expansion is done, but *, ?, and
    character ranges expressed with [] will be correctly matched.
    :return: yields a file path
    """
    directory = str(directory)
    log.info("Searching for %s in %s", pattern, directory)
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filePath = os.path.join(root, basename)
                log.info("found %s", filePath)
                yield filePath


if __name__ == '__main__':
    from junit_report_creator import log

    for filename in find_files('/tmp/pytest-of-robertobernabe/pytest-26/test_find0', '*.xml'):
        pass
