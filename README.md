Johnny the Cracker
==================

A simple password cracker

Usage
-----

$ johnny <TargetFile> <MaxPasswordLength> <OutputFile> [Type]

Requeriments
------------

+ pip install python-gnupg
+ pip install python-magic

Example
-------

```./johnny.py tests/secret.xyz.txt.gpg 4 secret.txt text/plain

Johnny the Cracker 0.1.0
Target file: tests/secret.xyz.txt.gpg
Maximum password length: 4
Output file: secret.txt


Creating 4 worker processes ...
Loading tests/secret.xyz.txt.gpg into memory ...
Creating password spaces ...
Starting password cracking ...

Process 16709 is cracking 1-character passwords [PS: size=36 interval=(0, z)]
Process 16710 is cracking 2-character passwords [PS: size=1296 interval=(00, zz)]
Process 16712 is cracking 3-character passwords [PS: size=10000 interval=(7ps, ffj)]
Process 16711 is cracking 3-character passwords [PS: size=10000 interval=(000, 7pr)]
Process 16709 is cracking 3-character passwords [PS: size=10000 interval=(ffk, n5b)]
Process 16710 is cracking 3-character passwords [PS: size=10000 interval=(n5c, uv3)]
Process 16712 is cracking 3-character passwords [PS: size=6656 interval=(uv4, zzz)]
Process 16711 is cracking 4-character passwords [PS: size=10000 interval=(0000, 07pr)]
Process 16709 is cracking 4-character passwords [PS: size=10000 interval=(07ps, 0ffj)]
Process 16710 is cracking 4-character passwords [PS: size=10000 interval=(0ffk, 0n5b)]
Process 16712 is cracking 4-character passwords [PS: size=10000 interval=(0n5c, 0uv3)]

Password found: xyz
Attempts: 45360
Elapsed time: 00:01:02
```

License
-------

Johnny is licensed under the GNU General Public License version 3, you should read LICENSE file to get more details about this.
