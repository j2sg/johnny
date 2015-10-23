#!/usr/bin/env python
# -*- coding: utf-8 -*-

"%s <target_file> <max_password_length> <output_file> [type]"
# See /usr/share/mime/types to get a list of all valid types.

import sys
import os
import os.path
from passwordspace import PasswordSpace
import gnupg
import magic
import time
import multiprocessing

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

    start = time.time()
    password, tested = crackMP(targetFileName, int(maxPasswordLength), outputFileName, outputFileType)
    end = time.time()

    print 'Password {0} after {1} seconds and {2} attempts'.format('not found' if password is None else '{0} found'.format(password), round(end - start, 3), tested)


def crack(targetFileName, maxPasswordLength, outputFileName, outputFileType):
    lowerCase = [chr(ascii) for ascii in range(ord('a'), ord('z') + 1)]
    upperCase = [chr(ascii) for ascii in range(ord('A'), ord('Z') + 1)]
    numbers = [chr(ascii) for ascii in range(ord('0'), ord('9') + 1)]
    password = None
    totalTested = 0

    with open(targetFileName, 'rb') as targetFile:
        encryptedData = targetFile.read()

    for passwordLength in range(1, maxPasswordLength + 1):
        password, tested = evalPasswordSpace(PasswordSpace(lowerCase + upperCase + numbers, passwordLength), encryptedData, outputFileName, outputFileType)
        totalTested += tested

        if not password is None:
            break

    return (password, totalTested)


def crackMP(targetFileName, maxPasswordLength, outputFileName, outputFileType):
    lowerCase = [chr(ascii) for ascii in range(ord('a'), ord('z') + 1)]
    upperCase = [chr(ascii) for ascii in range(ord('A'), ord('Z') + 1)]
    numbers = [chr(ascii) for ascii in range(ord('0'), ord('9') + 1)]
    password = None
    totalTested = 0

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    with open(targetFileName, 'rb') as targetFile:
        encryptedData = targetFile.read()

    passwordSpaces = []

    for passwordLength in range(1, maxPasswordLength + 1):
        passwordSpace = PasswordSpace(lowerCase + upperCase + numbers, passwordLength)

        if passwordSpace.maxPassword <= maxChunkSize:
            passwordSpaces.append(passwordSpace)
        else:
            passwordSpaces.extend(passwordSpace.split(maxChunkSize))

    tasks = [pool.apply_async(evalPasswordSpace, args=(passwordSpace, encryptedData, outputFileName, outputFileType,)) for passwordSpace in passwordSpaces]

    found = False
    finished = [False for t in range(len(tasks))]

    while not found:
        for k in range(len(tasks)):
            tasks[k].wait(timeout = 0.2)
            if tasks[k].ready():
                result = tasks[k].get()
                finished[k] = True

                if not result is None:
                    password, tested = result
                    totalTested += tested

                    if not password is None:
                        found = True

            if found:
                pool.terminate()
                break

        if reduce(lambda x, y: x and y, finished):
            break

    return (password, totalTested)


def evalPasswordSpace(passwordSpace, encryptedData, outputFileName, outputFileType):
    gpg = gnupg.GPG()
    tested = 0

    print 'Process {0} is cracking {1}-character passwords [size: {2} interval: ({3}, {4})]'.format(os.getpid(),
                                                                                                    passwordSpace.length,
                                                                                                    passwordSpace.maxPassword - passwordSpace.currentPassword,
                                                                                                    passwordSpace.alphaPassword(passwordSpace.currentPassword),
                                                                                                    passwordSpace.alphaPassword(passwordSpace.maxPassword - 1))

    for password in passwordSpace:
        result = gpg.decrypt(encryptedData, passphrase = password, output = outputFileName)

        if result.ok:
            if not os.path.isfile(outputFileName) or (not outputFileType is None and magic.from_file(outputFileName, mime = True) != outputFileType):
                continue

            return (password, tested)

        tested += 1

    return (None, tested)


if __name__ == '__main__':
    main()
