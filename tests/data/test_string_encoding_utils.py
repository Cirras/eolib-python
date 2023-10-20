import pytest
from collections import namedtuple
from eolib.data.string_encoding_utils import encode_string, decode_string

TCase = namedtuple("TCase", ["decoded", "encoded"])

TEST_CASES = [
    TCase("Hello, World!", "!;a-^H s^3a:)"),
    TCase(
        "We're ¼ of the way there, so ¾ is remaining.",
        "C8_6_6l2h- ,d ¾ ^, sh-h7Y T>V h7Y g0 ¼ :[xhH",
    ),
    TCase("64² = 4096", ";fAk b ²=i"),
    TCase("© FÒÖ BÃR BÅZ 2014", "=nAm EÅ] MÃ] ÖÒY ©"),
    TCase('Öxxö Xööx "Lëïth Säë" - "Ÿ"', "OŸO D OëäL 7YïëSO UööG öU'Ö"),
    TCase("Padded with 0xFFÿÿÿÿÿÿÿÿ", "ÿÿÿÿÿÿÿÿ+YUo 7Y6V i:i;lO"),
]


def idfn(test_case: TCase) -> str:
    return str(test_case.decoded)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=idfn)
def test_encode_string(test_case: TCase) -> None:
    decoded_bytes = bytearray(test_case.decoded, "windows-1252")

    encode_string(decoded_bytes)
    encoded = decoded_bytes.decode("windows-1252")

    assert encoded == test_case.encoded


@pytest.mark.parametrize("test_case", TEST_CASES, ids=idfn)
def test_decode_string(test_case: TCase) -> None:
    encoded_bytes = bytearray(test_case.encoded, "windows-1252")

    decode_string(encoded_bytes)
    decoded = encoded_bytes.decode("windows-1252")

    assert decoded == test_case.decoded
