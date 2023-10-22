class SerializationError(Exception):
    """
    Represents an error in serializing a protocol data structure.
    """

    def __init__(self, message: str):
        """
        Constructs a SerializationError with the specified error message.

        Args:
            message (str): The error message.
        """
        super().__init__(message)
