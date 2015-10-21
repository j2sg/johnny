#!/usr/bin/env python
# -*- coding: utf-8 -*-

"%s <target_file> <max_password_length> <output_file>"

import sys
import os
import os.path
from passwordspace import PasswordSpace
import gnupg

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
        crack(targetFileName, int(maxPasswordLength), outputFileName)
    except KeyboardInterrupt:
        print 'Process aborted by user'


def crack(targetFileName, maxPasswordLength, outputFileName):
    lowerCase = [chr(ascii) for ascii in range(ord('a'), ord('z') + 1)]
    upperCase = [chr(ascii) for ascii in range(ord('A'), ord('Z') + 1)]
    numbers = [chr(ascii) for ascii in range(ord('0'), ord('9') + 1)]
    alphabet = lowerCase + upperCase + numbers

    gpg = gnupg.GPG()

    tested = 0

    for passwordLength in range(1, maxPasswordLength + 1):
        print 'Generating passwords of {0} characters ...'.format(passwordLength)
        for password in PasswordSpace(alphabet, passwordLength):
            with open(targetFileName, 'rb') as targetFile:
                result = gpg.decrypt_file(targetFile, passphrase = password, output = outputFileName)

            if result.ok:
                print 'Password Found: {0}\nAttempts: {1}'.format(password, tested)
                sys.exit(0)

            tested += 1

    print 'Password not Found after {0} attempts\nYou must increase maximum password length'.format(tested)


if __name__ == '__main__':
    main()
