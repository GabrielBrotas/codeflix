#pylint: disable=protected-access
from abc import ABC
from dataclasses import FrozenInstanceError, dataclass, is_dataclass
import unittest
from unittest.mock import patch
import uuid
from core._shared.exceptions import InvalidUUIDException
from core._shared.value_objects import UniqueEntityId, ValueObject


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProp(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_an_abstract_class(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, 'value')

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual(vo2.prop1, 'value1')
        self.assertEqual(vo2.prop2, 'value2')

    def test_convert_to_string(self):
        vo1 = StubOneProp(prop='value')
        self.assertEqual(vo1.prop, str(vo1))

        vo2 = StubTwoProp(prop1='value1', prop2='value2')
        self.assertEqual(str(vo2), '{"prop1": "value1", "prop2": "value2"}')

    def test_if_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            vo1 = StubOneProp(prop='value')
            vo1.prop = "asd"


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_expection_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            # we have to specify like this because is a private method
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:

            with self.assertRaises(InvalidUUIDException) as assert_error:
                UniqueEntityId("fake id")

            mock_validate.assert_called_once()

            self.assertEqual(
                assert_error.exception.args[0], "ID must be a valid UUID")

    def test_if_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            # we have to specify like this because is a private method
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId(
                "c7fbfc54-c5de-4337-ab7b-72e9915fc545")
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, "c7fbfc54-c5de-4337-ab7b-72e9915fc545")

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_if_generate_id_without_pass_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            # we have to specify like this because is a private method
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_if_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "asd"
