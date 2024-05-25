"""
Al custom exceptions
"""


class InconsistentState(Exception):
    """
    Thrown whenever a board reaches an inconsistent state
    were piece and color arrays do not fit
    """
