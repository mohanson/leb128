# https://en.wikipedia.org/wiki/LEB128
#
# LEB128 or Little Endian Base 128 is a form of variable-length code
# compression used to store an arbitrarily large integer in a small number of
# bytes. LEB128 is used in the DWARF debug file format and the WebAssembly
# binary encoding for all integer literals.

import typing


class _U:
    @staticmethod
    def encode(i: int) -> bytearray:
        assert i >= 0
        r = []
        while True:
            byte = i & 0x7f
            i = i >> 7
            if i == 0:
                r.append(byte)
                return bytearray(r)
            r.append(0x80 | byte)

    @staticmethod
    def decode(b: bytearray) -> int:
        r = 0
        for i, e in enumerate(b):
            r = r + ((e & 0x7f) << (i * 7))
        return r

    @staticmethod
    def decode_reader(r: typing.BinaryIO) -> (int, int):
        a = bytearray()
        while True:
            b = ord(r.read(1))
            a.append(b)
            if (b & 0x80) == 0:
                break
        return _U.decode(a), len(a)


class _I:
    @staticmethod
    def encode(i: int) -> bytearray:
        r = []
        while True:
            byte = i & 0x7f
            i = i >> 7
            if (i == 0 and byte & 0x40 == 0) or (i == -1 and byte & 0x40 != 0):
                r.append(byte)
                return bytearray(r)
            r.append(0x80 | byte)

    @staticmethod
    def decode(b: bytearray) -> int:
        r = 0
        for i, e in enumerate(b):
            r = r + ((e & 0x7f) << (i * 7))
        if e & 0x40 != 0:
            r |= - (1 << (i * 7) + 7)
        return r

    @staticmethod
    def decode_reader(r: typing.BinaryIO) -> (int, int):
        a = bytearray()
        while True:
            b = ord(r.read(1))
            a.append(b)
            if (b & 0x80) == 0:
                break
        return _I.decode(a), len(a)


u = _U()
i = _I()
