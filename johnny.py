#!/usr/bin/env python
# -*- coding: utf-8 -*-

"%s <target_file> <max_password_length> <output_file> [type]"
# See /usr/share/mime/types to get a list of all valid types.

import sys
import os.path
from passwordspace import PasswordSpace
import gnupg
import magic
import time

def main():
    if len(sys.argv) < 4:
        print __doc__ % sys.argv[0]
        sys.exit(1)

    targetFileName = sys.argv[1]
    maxPasswordLength = sys.argv[2]
    outputFileName = sys.argv[3]
    outputFileType = None if len(sys.argv) != 5 else sys.argv[4]

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
        start = time.time()

        password, tested = crack(targetFileName, int(maxPasswordLength), outputFileName, outputFileType)

        end = time.time()

        if not password is None:
            print 'Password {0} found after {1} attempts for {2} seconds'.format(password, tested, round(end - start, 3))
        else:
            print 'Password not found after {0} attempts for {1} seconds'.format(tested, round(end - start, 3))
    except KeyboardInterrupt:
        print 'Process aborted by user'


def crack(targetFileName, maxPasswordLength, outputFileName, outputFileType):
    lowerCase = [chr(ascii) for ascii in range(ord('a'), ord('z') + 1)]
    upperCase = [chr(ascii) for ascii in range(ord('A'), ord('Z') + 1)]
    numbers = [chr(ascii) for ascii in range(ord('0'), ord('9') + 1)]
    password = None
    totalTested = 0

    for passwordLength in range(1, maxPasswordLength + 1):
        password, tested = evalPasswordSpace(PasswordSpace(lowerCase + upperCase + numbers, passwordLength), targetFileName, outputFileName, outputFileType)
        totalTested += tested

        if not password is None:
            break

    return (password, totalTested)


def evalPasswordSpace(passwordSpace, targetFileName, outputFileName, outputFileType):
    gpg = gnupg.GPG()
    tested = 0

    for password in passwordSpace:
        with open(targetFileName, 'rb') as targetFile:
            result = gpg.decrypt_file(targetFile, passphrase = password, output = outputFileName)

        if result.ok:
            if not os.path.isfile(outputFileName) or (not outputFileType is None and magic.from_file(outputFileName, mime = True) != outputFileType):
                continue

            return (password, tested)

        tested += 1

    return (None, tested)


if __name__ == '__main__':
    main()
