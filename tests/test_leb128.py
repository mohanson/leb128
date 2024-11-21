import io

import pytest

from leb128 import i, u


@pytest.mark.parametrize(
    ("arg", "ans"),
    [
        (0, bytearray([0x00])),
        (624485, bytearray([0xE5, 0x8E, 0x26])),
    ],
)
def test_unsigned_minimal(arg: int, ans: bytearray):
    assert u.encode(arg) == ans
    assert u.decode(ans) == arg
    assert u.decode_reader(io.BytesIO(ans)) == (arg, len(ans))


@pytest.mark.parametrize(
    ("arg", "ans"),
    [
        (0, bytearray([0x00])),
        (624485, bytearray([0xE5, 0x8E, 0x26])),
        (-12345, bytearray([0xC7, 0x9F, 0x7F])),
    ],
)
def test_signed_minimal(arg: int, ans: bytearray):
    assert i.encode(arg) == ans
    assert i.decode(ans) == arg
    assert i.decode_reader(io.BytesIO(ans)) == (arg, len(ans))


@pytest.mark.parametrize("lebject", [i, u])
def test_eof(lebject):
    reader = io.BytesIO(bytearray())

    with pytest.raises(EOFError):
        lebject.decode_reader(reader)


def test_u():
    with open("./test/u_case.txt") as f:
        for line in f:
            line = line.rstrip()
            seps = line.split()
            number = int(seps[0])
            binarr = bytearray.fromhex(seps[1])

            assert u.encode(number) == binarr
            assert u.decode(binarr) == number
            assert u.decode_reader(io.BytesIO(binarr)) == (number, len(binarr))


def test_i():
    with open("./test/i_case.txt") as f:
        for line in f:
            line = line.rstrip()
            seps = line.split()
            number = int(seps[0])
            binarr = bytearray.fromhex(seps[1])

            assert i.encode(number) == binarr
            assert i.decode(binarr) == number
            assert i.decode_reader(io.BytesIO(binarr)) == (number, len(binarr))
