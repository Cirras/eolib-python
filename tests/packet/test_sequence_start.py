import math
from eolib.packet.sequence_start import (
    SequenceStart,
    AccountReplySequenceStart,
    InitSequenceStart,
    PingSequenceStart,
)


def randrange_midpoint(a, b):
    return math.ceil((a + b) / 2)


def test_zero():
    assert SequenceStart.zero().value == 0


def test_account_reply_from_value():
    sequence_start = AccountReplySequenceStart.from_value(22)
    assert sequence_start.value == 22


def test_account_reply_generate(monkeypatch):
    monkeypatch.setattr('random.randrange', randrange_midpoint)

    sequence_start = AccountReplySequenceStart.generate()
    assert sequence_start.value == 120


def test_init__from_init_values():
    sequence_start = InitSequenceStart.from_init_values(110, 122)
    assert sequence_start.value == 879
    assert sequence_start.seq1 == 110
    assert sequence_start.seq2 == 122


def test_init_generate(monkeypatch):
    monkeypatch.setattr('random.randrange', randrange_midpoint)

    sequence_start = InitSequenceStart.generate()
    assert sequence_start.value == 879
    assert sequence_start.seq1 == 110
    assert sequence_start.seq2 == 122


def test_ping_from_ping_values():
    sequence_start = PingSequenceStart.from_ping_values(1005, 126)
    assert sequence_start.value == 879
    assert sequence_start.seq1 == 1005
    assert sequence_start.seq2 == 126


def test_ping_generate(monkeypatch):
    monkeypatch.setattr('random.randrange', randrange_midpoint)

    sequence_start = PingSequenceStart.generate()
    assert sequence_start.value == 879
    assert sequence_start.seq1 == 1005
    assert sequence_start.seq2 == 126
