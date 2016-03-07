import os
import glob
import logging
import pathlib

log = logging.getLogger()


def find(dirPathToSearch, pattern):
    """Searching for pattern in specific directory.
    Returns an list with found files and directories according to
    given pattern.

    :param dirPathToSearch:
    :param pattern: No tilde expansion is done, but *, ?, and
    character ranges expressed with [] will be correctly matched.
    :return: list of filepaths
    """
    p = os.path.join(dirPathToSearch, pattern)
    log.info("Searching for %s", p)
    _ = glob.glob(p)
    log.info("Found %s items with the pattern %s in %s:\n%s",
             len(_), pattern, dirPathToSearch, "\n".join(_))
    return _



if __name__ == '__main__':
    from junit_report_creator import log
    find("/home/robertobernabe/", "**/*")