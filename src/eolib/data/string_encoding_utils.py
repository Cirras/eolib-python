def encode_string(bytes: bytearray) -> None:
    """
    Encodes a string by inverting the bytes and then reversing them.

    This is an in-place operation.

    Args:
        bytes (bytearray): The byte array to encode.
    """
    _invert_characters(bytes)
    bytes.reverse()


def decode_string(bytes: bytearray) -> None:
    """
    Decodes a string by reversing the bytes and then inverting them.

    This is an in-place operation.

    Args:
        bytes (bytearray): The byte array to decode.
    """
    bytes.reverse()
    _invert_characters(bytes)


def _invert_characters(bytes: bytearray) -> None:
    """
    Inverts characters in a byte array.

    This is an in-place operation.

    Args:
        bytes (bytearray): The byte array to invert.
    """
    flippy = len(bytes) % 2 == 1

    for i in range(len(bytes)):
        c = bytes[i]
        f = 0

        if flippy:
            f = 0x2E
            if c >= 0x50:
                f *= -1

        if 0x22 <= c <= 0x7E:
            bytes[i] = 0x9F - c - f

        flippy = not flippy
