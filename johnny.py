#!/usr/bin/env python
# -*- coding: utf-8 -*-

"%s <target_file> <max_password_length> <output_file>"

import sys

def main():
    if len(sys.argv) != 4:
        print __doc__ % sys.argv[0]
        sys.exit(1)

if __name__ == '__main__':
    main()
