import io
from pathlib import Path

import pytest

from leb128 import i, u


CASE_FILES_DIR = Path(__file__).parent / "case_files"

I_CASE_FILE = CASE_FILES_DIR / "i_case.txt"
U_CASE_FILE = CASE_FILES_DIR / "u_case.txt"


def _assert_codec(codec, in_, out) -> None:
    assert codec.encode(in_) == out
    assert codec.decode(out) == in_
    assert codec.decode_reader(io.BytesIO(out)) == (in_, len(out))


@pytest.mark.parametrize(
    ("arg", "ans"),
    [
        (0, bytearray([0x00])),
        (624485, bytearray([0xE5, 0x8E, 0x26])),
    ],
)
def test_unsigned_minimal(arg: int, ans: bytearray):
    _assert_codec(u, arg, ans)


@pytest.mark.parametrize(
    ("arg", "ans"),
    [
        (0, bytearray([0x00])),
        (624485, bytearray([0xE5, 0x8E, 0x26])),
        (-12345, bytearray([0xC7, 0x9F, 0x7F])),
    ],
)
def test_signed_minimal(arg: int, ans: bytearray):
    _assert_codec(i, arg, ans)


@pytest.mark.parametrize("lebject", [i, u])
def test_eof(lebject):
    reader = io.BytesIO(bytearray())

    with pytest.raises(EOFError):
        lebject.decode_reader(reader)


@pytest.mark.parametrize(
    ("case_filepath", "leb"),
    [
        (I_CASE_FILE, i),
        (U_CASE_FILE, u),
    ],
)
def test_case_files(case_filepath: Path, leb):
    with open(case_filepath) as f:
        for line in f:
            line = line.rstrip()
            seps = line.split()
            number = int(seps[0])
            binarr = bytearray.fromhex(seps[1])

            _assert_codec(leb, number, binarr)
