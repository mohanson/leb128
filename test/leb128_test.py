import io
import random

import leb128


def test_u():
    for case_arg, case_out in [
        [0, bytearray([0x00])],
        [624485, bytearray([0xe5, 0x8e, 0x26])],
    ]:
        assert leb128.u.encode(case_arg) == case_out
        assert leb128.u.decode(case_out) == case_arg
        assert leb128.u.decode_reader(io.BytesIO(case_out)) == (case_arg, len(case_out))


def test_i():
    for case_arg, case_out in [
        [0, bytearray([0x00])],
        [624485, bytearray([0xe5, 0x8e, 0x26])],
        [-123456, bytearray([0xc0, 0xbb, 0x78])],
    ]:
        assert leb128.i.encode(case_arg) == case_out
        assert leb128.i.decode(case_out) == case_arg
        assert leb128.i.decode_reader(io.BytesIO(case_out)) == (case_arg, len(case_out))


def test_random():
    for _ in range(1 << 16):
        a = random.randint(+0x0000000000000000, +0xffffffffffffffff)
        b = leb128.u.encode(a)
        c = leb128.u.decode(b)
        assert a == c
    for _ in range(1 << 16):
        a = random.randint(-0xffffffffffffffff, +0xffffffffffffffff)
        b = leb128.i.encode(a)
        c = leb128.i.decode(b)
        assert a == c


if __name__ == '__main__':
    print('test_u')
    test_u()
    print('test_i')
    test_i()
    print('test_random')
    test_random()
