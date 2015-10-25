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

import math

class PasswordSpace:
    def __init__(self, alphabet, length):
        self.alphabet = alphabet
        self.length = length
        self.currentPassword = 0
        self.maxPassword = int(math.pow(len(self.alphabet), self.length))


    def __iter__(self):
        return self


    def next(self):
        if self.currentPassword == self.maxPassword:
            raise StopIteration
        else:
            result = self.alphaPassword(self.currentPassword)
            self.currentPassword += 1
            return result


    def alphaPassword(self, numeric):
        result = ''
        alphabetLength = len(self.alphabet)
        password = numeric

        while password / alphabetLength >= 1:
            result = self.alphabet[password % alphabetLength] + result
            password /= alphabetLength

        return (self.alphabet[password] + result).rjust(self.length, self.alphabet[0])


    def split(self, chunkSize):
        if chunkSize <= 0:
            return None

        nchunks = int(math.ceil((self.maxPassword - self.currentPassword) / float(chunkSize)))
        chunks = []

        for chunk in range(nchunks):
            subPasswordSpace = PasswordSpace(self.alphabet, self.length)

            subPasswordSpace.currentPassword = chunk * chunkSize
            subPasswordSpace.maxPassword = subPasswordSpace.currentPassword + (chunkSize if chunk != (nchunks - 1) else (self.maxPassword - self.currentPassword) % chunkSize)

            chunks.append(subPasswordSpace)

        return chunks


    def __str__(self):
        return 'Length: {0} characters\nSize: {1} passwords\nAlphabet: {2} characters {3}\n'.format(self.length, self.maxPassword, len(self.alphabet), self.alphabet)
