# LEB128

LEB128 or Little Endian Base 128 is a form of variable-length code compression used to store an arbitrarily large integer in a small number of bytes. LEB128 is used in the DWARF debug file format and the WebAssembly binary encoding for all integer literals.

```sh
$ pip install leb128
```

# Example

```py
import io
import leb128

# unsigned leb128
assert leb128.u.encode(624485) == bytearray([0xe5, 0x8e, 0x26])
assert leb128.u.decode(bytearray([0xe5, 0x8e, 0x26])) == 624485
assert leb128.u.decode_reader(io.BytesIO(bytearray([0xe5, 0x8e, 0x26]))) == (624485, 3)

#   signed leb128
assert leb128.i.encode(-12345) == bytearray([0xc7, 0x9f, 0x7f])
assert leb128.i.decode(bytearray([0xc7, 0x9f, 0x7f])) == -12345
assert leb128.i.decode_reader(io.BytesIO(bytearray([0xc7, 0x9f, 0x7f]))) == (-12345, 3)
```

# License

MIT
