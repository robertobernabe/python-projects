import argparse
import logging


log = logging.getLogger()


if not log.handlers:
    import sys
    log.addHandler(logging.StreamHandler(stream=sys.stdout))
    log.setLevel(logging.INFO)




if __name__ == '__main__':
    main()