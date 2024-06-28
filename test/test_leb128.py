import io
import leb128
import pytest


def test_minimal():
    for case_arg, case_out in [
        [0, bytearray([0x00])],
        [624485, bytearray([0xe5, 0x8e, 0x26])],
    ]:
        assert leb128.u.encode(case_arg) == case_out
        assert leb128.u.decode(case_out) == case_arg
        assert leb128.u.decode_reader(io.BytesIO(case_out)) == (case_arg, len(case_out))
    for case_arg, case_out in [
        [0, bytearray([0x00])],
        [624485, bytearray([0xe5, 0x8e, 0x26])],
        [-12345, bytearray([0xc7, 0x9f, 0x7f])],
    ]:
        assert leb128.i.encode(case_arg) == case_out
        assert leb128.i.decode(case_out) == case_arg
        assert leb128.i.decode_reader(io.BytesIO(case_out)) == (case_arg, len(case_out))
    print(f'test_minimal')


def test_eof():
    reader = io.BytesIO(bytearray())
    with pytest.raises(EOFError):
        leb128.u.decode_reader(reader)
    reader = io.BytesIO(bytearray())
    with pytest.raises(EOFError):
        leb128.i.decode_reader(reader)


def test_u():
    n = 0
    with open('./test/u_case.txt', 'r') as f:
        for line in f:
            line = line.rstrip()
            seps = line.split()
            number = int(seps[0])
            binarr = bytearray.fromhex(seps[1])

            assert leb128.u.encode(number) == binarr
            assert leb128.u.decode(binarr) == number
            assert leb128.u.decode_reader(io.BytesIO(binarr)) == (number, len(binarr))
            n += 1
    print(f'test_u: {n} case')


def test_i():
    n = 0
    with open('./test/i_case.txt', 'r') as f:
        for line in f:
            line = line.rstrip()
            seps = line.split()
            number = int(seps[0])
            binarr = bytearray.fromhex(seps[1])

            assert leb128.i.encode(number) == binarr
            assert leb128.i.decode(binarr) == number
            assert leb128.i.decode_reader(io.BytesIO(binarr)) == (number, len(binarr))
            n += 1
    print(f'test_i: {n} case')


if __name__ == '__main__':
    test_minimal()
    test_u()
    test_i()
