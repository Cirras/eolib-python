import pytest
from collections import namedtuple
from eolib.data.eo_numeric_limits import THREE_MAX
from eolib.encrypt.server_verification_utils import server_verification_hash

TCase = namedtuple("TCase", ["challenge", "expected_hash"])


def idfn(test_case: TCase) -> str:
    return str(test_case.challenge)


@pytest.mark.parametrize(
    "test_case",
    [
        TCase(0, 114000),
        TCase(1, 115191),
        TCase(2, 229432),
        TCase(5, 613210),
        TCase(12345, 266403),
        TCase(100_000, 145554),
        TCase(5_000_000, 339168),
        TCase(11_092_003, 112773),
        TCase(11_092_004, 112655),
        TCase(11_092_005, 112299),
        TCase(11_092_110, 11016),
        TCase(11_092_111, -2787),
        TCase(11_111_111, 103749),
        TCase(12_345_678, -32046),
        TCase(THREE_MAX - 1, 105960),
    ],
    ids=idfn,
)
def test_server_verification_hash(test_case: TCase):
    challenge_hash = server_verification_hash(test_case.challenge)
    assert challenge_hash == test_case.expected_hash
