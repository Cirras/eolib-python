from eolib.protocol.serialization_error import SerializationError


def test_message():
    message = "Oh no, the sun exploded!"
    assert str(SerializationError(message)) == message
