import pytest
from typing import Iterable
from eolib import EoReader


def test_slice():
    reader = create_reader([0x01, 0x02, 0x03, 0x04, 0x05, 0x06])
    reader.get_byte()
    reader.chunked_reading_mode = True

    reader2 = reader.slice()
    assert reader2.position == 0
    assert reader2.remaining == 5
    assert not reader2.chunked_reading_mode

    reader3 = reader2.slice(1)
    assert reader3.position == 0
    assert reader3.remaining == 4
    assert not reader3.chunked_reading_mode

    reader4 = reader3.slice(1, 2)
    assert reader4.position == 0
    assert reader4.remaining == 2
    assert not reader4.chunked_reading_mode

    assert reader.position == 1
    assert reader.remaining == 5
    assert reader.chunked_reading_mode


def test_slice_over_read():
    reader = create_reader([0x01, 0x02, 0x03])
    assert reader.slice(2, 5).remaining == 1
    assert reader.slice(3).remaining == 0
    assert reader.slice(4).remaining == 0
    assert reader.slice(4, 12345).remaining == 0


def test_slice_negative_index():
    reader = create_reader([0x01, 0x02, 0x03])
    with pytest.raises(ValueError):
        reader.slice(-1)


def test_slice_negative_length():
    reader = create_reader([0x01, 0x02, 0x03])
    with pytest.raises(ValueError):
        reader.slice(0, -1)


@pytest.mark.parametrize("byte_value", [0x00, 0x01, 0x02, 0x80, 0xFD, 0xFE, 0xFF])
def test_get_byte(byte_value: int):
    reader = create_reader([byte_value])
    assert reader.get_byte() == byte_value


def test_over_read_byte():
    reader = create_reader([])
    assert reader.get_byte() == 0x00


def test_get_bytes():
    reader = create_reader([0x01, 0x02, 0x03, 0x04, 0x05])
    assert reader.get_bytes(3) == bytes([0x01, 0x02, 0x03])
    assert reader.get_bytes(10) == bytes([0x04, 0x05])
    assert reader.get_bytes(1) == bytes([])


def test_get_char():
    reader = create_reader([0x01, 0x02, 0x80, 0x81, 0xFD, 0xFE, 0xFF])
    assert reader.get_char() == 0
    assert reader.get_char() == 1
    assert reader.get_char() == 127
    assert reader.get_char() == 128
    assert reader.get_char() == 252
    assert reader.get_char() == 0
    assert reader.get_char() == 254


def test_get_short():
    reader = create_reader(
        [0x01, 0xFE, 0x02, 0xFE, 0x80, 0xFE, 0xFD, 0xFE, 0xFE, 0xFE, 0xFE, 0x80, 0x7F, 0x7F, 0xFD]
        + [0xFD]
    )
    assert reader.get_short() == 0
    assert reader.get_short() == 1
    assert reader.get_short() == 127
    assert reader.get_short() == 252
    assert reader.get_short() == 0
    assert reader.get_short() == 0
    assert reader.get_short() == 32004
    assert reader.get_short() == 64008


def test_get_three():
    reader = create_reader(
        [0x01, 0xFE, 0xFE, 0x02, 0xFE, 0xFE, 0x80, 0xFE, 0xFE, 0xFD, 0xFE, 0xFE, 0xFE, 0xFE, 0xFE]
        + [0xFE, 0x80, 0x81, 0x7F, 0x7F, 0xFE, 0xFD, 0xFD, 0xFE, 0xFD, 0xFD, 0xFD]
    )
    assert reader.get_three() == 0
    assert reader.get_three() == 1
    assert reader.get_three() == 127
    assert reader.get_three() == 252
    assert reader.get_three() == 0
    assert reader.get_three() == 0
    assert reader.get_three() == 32004
    assert reader.get_three() == 64008
    assert reader.get_three() == 16194276


def test_get_int():
    reader = create_reader(
        [0x01, 0xFE, 0xFE, 0xFE, 0x02, 0xFE, 0xFE, 0xFE, 0x80, 0xFE, 0xFE, 0xFE, 0xFD, 0xFE, 0xFE]
        + [0xFE, 0xFE, 0xFE, 0xFE, 0xFE, 0xFE, 0x80, 0x81, 0x82, 0x7F, 0x7F, 0xFE, 0xFE, 0xFD, 0xFD]
        + [0xFE, 0xFE, 0xFD, 0xFD, 0xFD, 0xFE, 0x7F, 0x7F, 0x7F, 0x7F, 0xFD, 0xFD, 0xFD, 0xFD]
    )
    assert reader.get_int() == 0
    assert reader.get_int() == 1
    assert reader.get_int() == 127
    assert reader.get_int() == 252
    assert reader.get_int() == 0
    assert reader.get_int() == 0
    assert reader.get_int() == 32004
    assert reader.get_int() == 64008
    assert reader.get_int() == 16194276
    assert reader.get_int() == 2048576040
    assert reader.get_int() == 4097152080


def test_get_string():
    reader = create_reader(b"Hello, World!")
    assert reader.get_string() == "Hello, World!"


def test_get_fixed_string():
    reader = create_reader(b"foobar")
    assert reader.get_fixed_string(3) == "foo"
    assert reader.get_fixed_string(3) == "bar"


def test_padded_get_fixed_string():
    reader = create_reader(bytes("fooÿbarÿÿÿ", "windows-1252"))
    assert reader.get_fixed_string(4, True) == "foo"
    assert reader.get_fixed_string(6, True) == "bar"


def test_chunked_get_string():
    reader = create_reader(bytes("Hello,ÿWorld!", "windows-1252"))
    reader.chunked_reading_mode = True

    assert reader.get_string() == "Hello,"

    reader.next_chunk()
    assert reader.get_string() == "World!"


def test_get_negative_length_string():
    reader = create_reader(b"foo")
    with pytest.raises(ValueError):
        reader.get_fixed_string(-1)


def test_get_encoded_string():
    reader = create_reader(b"!;a-^H s^3a:)")
    assert reader.get_encoded_string() == "Hello, World!"


def test_fixed_get_encoded_string():
    reader = create_reader(b"^0g[>k")
    assert reader.get_fixed_encoded_string(3) == "foo"
    assert reader.get_fixed_encoded_string(3) == "bar"


def test_padded_get_fixed_encoded_string():
    reader = create_reader(bytes("ÿ0^9ÿÿÿ-l=S>k", "windows-1252"))
    assert reader.get_fixed_encoded_string(4, True) == "foo"
    assert reader.get_fixed_encoded_string(6, True) == "bar"
    assert reader.get_fixed_encoded_string(3, True) == "baz"


def test_chunked_get_encoded_string():
    reader = create_reader(bytes("E0a3hWÿ!;a-^H", "windows-1252"))
    reader.chunked_reading_mode = True

    assert reader.get_encoded_string() == "Hello,"

    reader.next_chunk()
    assert reader.get_encoded_string() == "World!"


def test_get_negative_length_encoded_string():
    reader = create_reader(b"^0g")
    with pytest.raises(ValueError):
        reader.get_fixed_encoded_string(-1)


def test_chunked_reading_mode():
    reader = create_reader([])
    assert not reader.chunked_reading_mode
    reader.chunked_reading_mode = True
    assert reader.chunked_reading_mode


def test_remaining():
    reader = create_reader([0x01, 0x03, 0x04, 0xFE, 0x05, 0xFE, 0xFE, 0x06, 0xFE, 0xFE, 0xFE])

    assert reader.remaining == 11
    reader.get_byte()
    assert reader.remaining == 10
    reader.get_char()
    assert reader.remaining == 9
    reader.get_short()
    assert reader.remaining == 7
    reader.get_three()
    assert reader.remaining == 4
    reader.get_int()
    assert reader.remaining == 0

    reader.get_char()
    assert reader.remaining == 0


def test_chunked_remaining():
    reader = create_reader([0x01, 0x03, 0x04, 0xFF, 0x05, 0xFE, 0xFE, 0x06, 0xFE, 0xFE, 0xFE])
    reader.chunked_reading_mode = True

    assert reader.remaining == 3
    reader.get_char()
    reader.get_short()
    assert reader.remaining == 0

    reader.get_char()
    assert reader.remaining == 0

    reader.next_chunk()
    assert reader.remaining == 7


def test_next_chunk():
    reader = create_reader([0x01, 0x02, 0xFF, 0x03, 0x04, 0x5, 0xFF, 0x06])
    reader.chunked_reading_mode = True

    assert reader.position == 0

    reader.next_chunk()
    assert reader.position == 3

    reader.next_chunk()
    assert reader.position == 7

    reader.next_chunk()
    assert reader.position == 8

    reader.next_chunk()
    assert reader.position == 8


def test_next_chunk_not_in_chunked_reading_mode():
    reader = create_reader([0x01, 0x02, 0xFF, 0x03, 0x04, 0x5, 0xFF, 0x06])
    with pytest.raises(RuntimeError):
        reader.next_chunk()


def test_next_chunk_with_chunked_reading_toggled_in_between():
    reader = create_reader([0x01, 0x02, 0xFF, 0x03, 0x04, 0x5, 0xFF, 0x06])
    assert reader.position == 0

    reader.chunked_reading_mode = True
    reader.next_chunk()
    reader.chunked_reading_mode = False
    assert reader.position == 3

    reader.chunked_reading_mode = True
    reader.next_chunk()
    reader.chunked_reading_mode = False
    assert reader.position == 7

    reader.chunked_reading_mode = True
    reader.next_chunk()
    reader.chunked_reading_mode = False
    assert reader.position == 8

    reader.chunked_reading_mode = True
    reader.next_chunk()
    reader.chunked_reading_mode = False
    assert reader.position == 8


def test_under_read():
    reader = create_reader([0x7C, 0x67, 0x61, 0x72, 0x62, 0x61, 0x67, 0x65, 0xFF, 0xCA, 0x31])
    reader.chunked_reading_mode = True

    assert reader.get_char() == 123
    reader.next_chunk()
    assert reader.get_short() == 12345


def test_over_read():
    reader = create_reader([0xFF, 0x7C])
    reader.chunked_reading_mode = True

    assert reader.get_int() == 0
    reader.next_chunk()
    assert reader.get_short() == 123


def test_double_read():
    reader = create_reader([0xFF, 0x7C, 0xCA, 0x31])

    assert reader.get_int() == 790222478

    reader.chunked_reading_mode = True
    reader.next_chunk()
    assert reader.get_char() == 123
    assert reader.get_short() == 12345


def create_reader(input_data: Iterable[int]) -> EoReader:
    data = bytearray(10)
    data.extend(input_data)
    data.extend([0] * 10)

    return EoReader(data).slice(10, len(data) - 20)
