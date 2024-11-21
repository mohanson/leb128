"""
https://en.wikipedia.org/wiki/LEB128

LEB128 or Little Endian Base 128 is a form of variable-length code
compression used to store an arbitrarily large integer in a small number of
bytes. LEB128 is used in the DWARF debug file format and the WebAssembly
binary encoding for all integer literals.
"""

import typing


class Leb128Error(Exception):
    pass


class _U:
    """Unsigned LEB128 codec."""

    @staticmethod
    def encode(i: int) -> bytearray:
        """Encode the int i using unsigned leb128 and return the encoded bytearray."""

        if i < 0:
            msg = f"{i} < 0"
            raise Leb128Error(msg)

        r = []
        while True:
            byte = i & 0x7F
            i = i >> 7
            if i == 0:
                r.append(byte)
                return bytearray(r)
            r.append(0x80 | byte)

    @staticmethod
    def decode(b: bytearray, *, check_empty: bool = False) -> int:
        """Decode the unsigned leb128 encoded bytearray."""

        if check_empty and not b:
            msg = f"cannot decode an empty bytearray {b}"
            raise Leb128Error(msg)

        r = 0
        for i, e in enumerate(b):
            r = r + ((e & 0x7F) << (i * 7))
        return r

    @staticmethod
    def decode_reader(r: typing.BinaryIO) -> typing.Tuple[int, int]:
        """Decode the unsigned leb128 encoded from a reader.

        It will return two values:
        - the actual number;
        - the number of bytes read.
        """

        a = bytearray()
        while True:
            b = r.read(1)
            if len(b) != 1:
                raise EOFError
            b = ord(b)
            a.append(b)
            if (b & 0x80) == 0:
                break
        return _U.decode(a), len(a)


class _I:
    """Signed LEB128 codec."""

    @staticmethod
    def encode(i: int) -> bytearray:
        """Encode the int i using signed leb128 and return the encoded bytearray."""

        r = []
        while True:
            byte = i & 0x7F
            i = i >> 7
            if (i == 0 and byte & 0x40 == 0) or (i == -1 and byte & 0x40 != 0):
                r.append(byte)
                return bytearray(r)
            r.append(0x80 | byte)

    @staticmethod
    def decode(b: bytearray, *, check_empty: bool = False) -> int:
        """Decode the signed leb128 encoded bytearray."""

        if check_empty and not b:
            msg = f"cannot decode an empty bytearray {b}"
            raise Leb128Error(msg)

        r = 0
        for i, e in enumerate(b):
            r = r + ((e & 0x7F) << (i * 7))
        if e & 0x40 != 0:
            r |= -(1 << (i * 7) + 7)
        return r

    @staticmethod
    def decode_reader(r: typing.BinaryIO) -> typing.Tuple[int, int]:
        """Decode the signed leb128 encoded from a reader.

        It will return two values:
        - the actual number
        - the number of bytes read.
        """

        a = bytearray()
        while True:
            b = r.read(1)
            if len(b) != 1:
                raise EOFError
            b = ord(b)
            a.append(b)
            if (b & 0x80) == 0:
                break
        return _I.decode(a), len(a)


u = _U()
i = _I()
