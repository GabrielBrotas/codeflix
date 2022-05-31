class InvalidUUIDException(Exception):

    # pylint: disable=useless-super-delegation
    def __init__(self, error='ID must be a valid UUID') -> None:
        super().__init__(error)
