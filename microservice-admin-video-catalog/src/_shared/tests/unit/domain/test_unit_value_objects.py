from dataclasses import is_dataclass
import unittest
from unittest.mock import patch
import uuid
from src._shared.domain.exceptions import InvalidUUIDException

from src._shared.domain.value_objects import UniqueEntityId


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_expection_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate", # we have to specify like this because is a private method
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:

            with self.assertRaises(InvalidUUIDException) as assert_error:
                UniqueEntityId("fake id")

            mock_validate.assert_called_once()

            self.assertEqual(assert_error.exception.args[0], "ID must be a valid UUID")
    
    def test_if_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate", # we have to specify like this because is a private method
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId("c7fbfc54-c5de-4337-ab7b-72e9915fc545")
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, "c7fbfc54-c5de-4337-ab7b-72e9915fc545")

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_if_generate_id_without_pass_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate", # we have to specify like this because is a private method
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()


        


    