#!/usr/bin/env python
# -*- coding: utf-8 -*-

"%s <target_file> <max_password_length> <output_file>"

import sys
import os.path

def main():
    if len(sys.argv) != 4:
        print __doc__ % sys.argv[0]
        sys.exit(1)

    targetFileName, maxPasswordLength, outputFileName = sys.argv[1:]

    if not os.path.isfile(targetFileName):
        print 'Error: {0} not found'.format(targetFileName)
        sys.exit(1)

    try:
        if int(maxPasswordLength) < 1:
            print 'Error: Maximum password length cannot be less than 1'
            sys.exit(1)
    except ValueError:
        print __doc__ % sys.argv[0]
        sys.exit(1)

    try:
        crack(targetFileName, maxPasswordLength, outputFileName)
    except KeyboardInterrupt:
        print 'Process aborted by user'


def crack(targetFileName, maxPasswordLength, outputFileName):
    pass


if __name__ == '__main__':
    main()
