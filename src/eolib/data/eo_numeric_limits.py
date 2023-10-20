"""
Constants for the maximum values of the EO numeric types.

The largest valid value for each type is TYPE_MAX - 1.
"""

CHAR_MAX = 253
"""
The maximum value of an EO char (1-byte encoded integer type).
"""

SHORT_MAX = CHAR_MAX * CHAR_MAX
"""
The maximum value of an EO short (2-byte encoded integer type).
"""

THREE_MAX = CHAR_MAX * CHAR_MAX * CHAR_MAX
"""
The maximum value of an EO three (3-byte encoded integer type).
"""

INT_MAX = CHAR_MAX * CHAR_MAX * CHAR_MAX * CHAR_MAX
"""
The maximum value of an EO int (4-byte encoded integer type).
"""
