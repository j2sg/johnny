#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of Johnny.
#
#  Copyright (c) 2015 Juan Jose Salazar Garcia jjslzgc@gmail.com
#
#  Johnny is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Johnny is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Johnny.  If not, see <http://www.gnu.org/licenses/>.
#

"%s <target_file> <max_password_length> <output_file> [type]"
# See /usr/share/mime/types to get a list of all valid types.

import sys
import os
import os.path
from passwordspace import PasswordSpace
import gnupg
import magic
import time
import datetime
import multiprocessing

APPLICATION_NAME = 'Johnny the Cracker'
APPLICATION_VERSION = '0.1.0'
maxChunkSize = 10000

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

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

    print '\n{0} {1}'.format(APPLICATION_NAME, APPLICATION_VERSION)
    print 'Target file: {0}'.format(targetFileName)
    print 'Maximum password length: {0}'.format(maxPasswordLength)
    print 'Output file: {0}\n'.format(outputFileName)

    if os.path.isfile(outputFileName):
        while True:
            response = raw_input('{0} already exists. do you want to replace it? [y/n]'.format(outputFileName))
            if response in ['y', 'Y', 'n', 'N']:
                break

        if response.lower() != 'y':
            sys.exit(0)
        else:
            os.remove(outputFileName)

    start = time.time()
    password, tested = crackMP(targetFileName, int(maxPasswordLength), outputFileName, outputFileType)
    end = time.time()

    print '\nPassword found: {0}'.format(password) if not password is None else '\nNo password found for {0}-character maximum length'.format(maxPasswordLength)
    print 'Attempts: {0}'.format(tested)
    print 'Elapsed time: {:0>8}'.format(datetime.timedelta(seconds = int(end - start)))


def crackMP(targetFileName, maxPasswordLength, outputFileName, outputFileType):
    lowerCase = [chr(ascii) for ascii in range(ord('a'), ord('z') + 1)]
    upperCase = [chr(ascii) for ascii in range(ord('A'), ord('Z') + 1)]
    numbers = [chr(ascii) for ascii in range(ord('0'), ord('9') + 1)]
    password = None
    totalTested = 0

    print '\nCreating {0} worker processes ...'.format(multiprocessing.cpu_count())

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    print 'Loading {0} into memory ...'.format(targetFileName)

    with open(targetFileName, 'rb') as targetFile:
        encryptedData = targetFile.read()

    print 'Creating password spaces ...'

    passwordSpaces = []

    for passwordLength in range(1, maxPasswordLength + 1):
        passwordSpace = PasswordSpace(lowerCase + upperCase + numbers, passwordLength)

        if passwordSpace.maxPassword <= maxChunkSize:
            passwordSpaces.append(passwordSpace)
        else:
            passwordSpaces.extend(passwordSpace.split(maxChunkSize))

    print 'Starting password cracking ...\n'

    tasks = [pool.apply_async(evalPasswordSpace, args=(passwordSpace, encryptedData, outputFileName, outputFileType,)) for passwordSpace in passwordSpaces]

    for task in tasks:
        password, tested = task.get()
        totalTested += tested

        if not password is None:
            pool.terminate()
            break

    return (password, totalTested)


def evalPasswordSpace(passwordSpace, encryptedData, outputFileName, outputFileType):
    gpg = gnupg.GPG()
    tested = 0

    print 'Process {0} is cracking {1}-character passwords [PS: size={2} interval=({3}, {4})]'.format(os.getpid(),
                                                                                                      passwordSpace.length,
                                                                                                      passwordSpace.maxPassword - passwordSpace.currentPassword,
                                                                                                      passwordSpace.alphaPassword(passwordSpace.currentPassword),
                                                                                                      passwordSpace.alphaPassword(passwordSpace.maxPassword - 1))

    for password in passwordSpace:
        result = gpg.decrypt(encryptedData, passphrase = password, output = outputFileName)

        tested += 1

        if result.ok:
            if not os.path.isfile(outputFileName) or (not outputFileType is None and magic.from_file(outputFileName, mime = True) != outputFileType):
                continue

            return (password, tested)

    return (None, tested)


if __name__ == '__main__':
    main()
