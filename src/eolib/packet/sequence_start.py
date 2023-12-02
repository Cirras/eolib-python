import random
from abc import ABC, abstractproperty
from eolib.data.eo_numeric_limits import CHAR_MAX


class SequenceStart(ABC):
    """
    A value sent by the server to update the client's sequence start, also known as the 'starting
    counter ID'.
    """

    @abstractproperty
    def value(self) -> int:
        """
        int: Gets the sequence start value.
        """
        raise NotImplementedError()

    @staticmethod
    def zero() -> 'SequenceStart':
        """
        Returns an instance of SequenceStart with a value of 0.

        Returns:
            SequenceStart: An instance of SequenceStart.
        """
        return SimpleSequenceStart(0)


class SimpleSequenceStart(SequenceStart):
    _value: int

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self):
        return self._value


class AccountReplySequenceStart(SimpleSequenceStart):
    """
    A class representing the sequence start value sent with the `ACCOUNT_REPLY` server packet.

    See Also:
        - [`AccountReplyServerPacket`][eolib.protocol._generated.net.server.AccountReplyServerPacket]
    """

    def __init__(self, value: int):
        super().__init__(value)

    @staticmethod
    def from_value(value: int) -> 'AccountReplySequenceStart':
        """
        Creates an instance of AccountReplySequenceStart from the value sent with the
        `ACCOUNT_REPLY` server packet.

        Args:
            value (int): The sequence start value sent with the `ACCOUNT_REPLY` server packet.

        Returns:
            AccountReplySequenceStart: An instance of AccountReplySequenceStart.
        """
        return AccountReplySequenceStart(value)

    @staticmethod
    def generate() -> 'AccountReplySequenceStart':
        """
        Generates an instance of AccountReplySequenceStart with a random value in the range 0-240.

        Returns:
            AccountReplySequenceStart: An instance of AccountReplySequenceStart.
        """
        return AccountReplySequenceStart(random.randrange(0, 240))


class InitSequenceStart(SimpleSequenceStart):
    """
    A class representing the sequence start value sent with the `INIT_INIT` server packet.

    See Also:
        - [`InitInitServerPacket`][eolib.protocol._generated.net.server.InitInitServerPacket]
    """

    _seq1: int
    _seq2: int

    def __init__(self, value: int, seq1: int, seq2: int):
        super().__init__(value)
        self._seq1 = seq1
        self._seq2 = seq2

    @property
    def seq1(self) -> int:
        """
        Returns the `seq1` byte value sent with the `INIT_INIT` server packet.

        Returns:
            int: The seq1 byte value.
        """
        return self._seq1

    @property
    def seq2(self) -> int:
        """
        Returns the `seq2` byte value sent with the `INIT_INIT` server packet.

        Returns:
            int: The seq2 byte value.
        """
        return self._seq2

    @staticmethod
    def from_init_values(seq1: int, seq2: int) -> 'InitSequenceStart':
        """
        Creates an instance of InitSequenceStart from the values sent with the `INIT_INIT` server
        packet.

        Args:
            seq1 (int): The `seq1` byte value sent with the `INIT_INIT` server packet.
            seq2 (int): The `seq2` byte value sent with the `INIT_INIT` server packet.

        Returns:
            InitSequenceStart: An instance of InitSequenceStart
        """
        value = seq1 * 7 + seq2 - 13
        return InitSequenceStart(value, seq1, seq2)

    @staticmethod
    def generate() -> 'InitSequenceStart':
        """
        Generates an instance of InitSequenceStart with a random value in the range 0-1757.

        Returns:
            InitSequenceStart: An instance of InitSequenceStart.
        """
        value = random.randrange(0, 1757)
        seq1_max = int((value + 13) / 7)
        seq1_min = max(0, int((value - (CHAR_MAX - 1) + 13 + 6) / 7))

        seq1 = random.randrange(0, seq1_max - seq1_min) + seq1_min
        seq2 = value - seq1 * 7 + 13

        return InitSequenceStart(value, seq1, seq2)


class PingSequenceStart(SimpleSequenceStart):
    """
    A class representing the sequence start value sent with the `CONNECTION_PLAYER` server packet.

    See Also:
        - [`ConnectionPlayerServerPacket`][eolib.protocol._generated.net.server.ConnectionPlayerServerPacket]
    """

    def __init__(self, value: int, seq1: int, seq2: int):
        super().__init__(value)
        self._seq1 = seq1
        self._seq2 = seq2

    @property
    def seq1(self) -> int:
        """
        Returns the seq1 short value sent with the `CONNECTION_PLAYER` server packet.

        Returns:
            int: The seq1 short value.
        """
        return self._seq1

    @property
    def seq2(self) -> int:
        """
        Returns the seq2 char value sent with the `CONNECTION_PLAYER` server packet.

        Returns:
            int: The seq2 char value.
        """
        return self._seq2

    @staticmethod
    def from_ping_values(seq1: int, seq2: int) -> 'PingSequenceStart':
        """
        Creates an instance of PingSequenceStart from the values sent with the `CONNECTION_PLAYER`
        server packet.

        Args:
            seq1 (int): The `seq1` short value sent with the `CONNECTION_PLAYER` server packet.
            seq2 (int): The `seq2` char value sent with the `CONNECTION_PLAYER` server packet.

        Returns:
            PingSequenceStart: An instance of PingSequenceStart.
        """
        value = seq1 - seq2
        return PingSequenceStart(value, seq1, seq2)

    @staticmethod
    def generate() -> 'PingSequenceStart':
        """
        Generates an instance of PingSequenceStart with a random value in the range 0-1757.

        Returns:
            PingSequenceStart: An instance of PingSequenceStart.
        """
        value = random.randrange(0, 1757)
        seq1 = value + random.randrange(0, CHAR_MAX - 1)
        seq2 = seq1 - value

        return PingSequenceStart(value, seq1, seq2)


__all__ = ['SequenceStart', 'AccountReplySequenceStart', 'InitSequenceStart', 'PingSequenceStart']
