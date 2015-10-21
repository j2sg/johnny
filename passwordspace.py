# -*- coding: utf-8 -*-

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
            result = self.alphaPassword()
            self.currentPassword += 1
            return result


    def alphaPassword(self):
        result = ''
        alphabetLength = len(self.alphabet)
        password = self.currentPassword

        while password / alphabetLength >= 1:
            result = self.alphabet[password % alphabetLength] + result
            password /= alphabetLength

        return (self.alphabet[password] + result).rjust(self.length, self.alphabet[0])


    def __str__(self):
        return 'Length: {0} characters\nSize: {1} passwords\nAlphabet: {2} characters {3}\n'.format(self.length, self.maxPassword, len(self.alphabet), self.alphabet)
