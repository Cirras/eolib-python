from eolib.packet.packet_sequencer import PacketSequencer
from eolib.packet.sequence_start import AccountReplySequenceStart


def test_next_sequence():
    sequence_start = AccountReplySequenceStart.from_value(123)
    sequencer = PacketSequencer(sequence_start)

    for i in range(10):
        assert sequencer.next_sequence() == 123 + i

    assert sequencer.next_sequence() == 123


def test_sequence_start():
    sequence_start = AccountReplySequenceStart.from_value(100)
    sequencer = PacketSequencer(sequence_start)

    assert sequencer.next_sequence() == 100

    sequencer.set_sequence_start(AccountReplySequenceStart.from_value(200))

    assert sequencer.next_sequence() == 201
