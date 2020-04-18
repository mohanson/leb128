# LEB128

LEB128 or Little Endian Base 128 is a form of variable-length code compression used to store an arbitrarily large integer in a small number of bytes. LEB128 is used in the DWARF debug file format and the WebAssembly binary encoding for all integer literals.

```sh
$ pip3 install leb128
```

# Usage

```py
import leb128

assert leb128.u.encode(624485) == bytearray([0xe5, 0x8e, 0x26])
assert leb128.u.decode(bytearray([0xe5, 0x8e, 0x26])) == 624485
assert leb128.i.encode(-123456) == bytearray([0xc0, 0xbb, 0x78])
assert leb128.i.decode(bytearray([0xc0, 0xbb, 0x78])) == -123456
```
