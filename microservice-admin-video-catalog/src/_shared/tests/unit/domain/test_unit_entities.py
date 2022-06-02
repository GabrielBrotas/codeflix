# pylint: disable=unexpected-keyword-arg,protected-access
from dataclasses import dataclass, is_dataclass
import unittest

from _shared.domain.entities import Entity
from _shared.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity()))

    def test_set_id_and_props(self):
        entity = StubEntity(prop1="value1", prop2="value2")

        self.assertEqual(entity.prop1, "value1")
        self.assertEqual(entity.prop2, "value2")
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_if_accept_uuid_in_parameters(self):
        entity = StubEntity(
            unique_entity_id="42bb40a2-b558-4794-b79e-f5085af808d1", prop1="value1", prop2="value2")
        self.assertEqual(entity.id, "42bb40a2-b558-4794-b79e-f5085af808d1")

    def test_to_dict_method(self):
        id_value = "42bb40a2-b558-4794-b79e-f5085af808d1"
        entity = StubEntity(
            unique_entity_id=id_value,
            prop1="value1",
            prop2="value2"
        )

        self.assertDictEqual(entity.to_dict(), {
            'id': id_value,
            'prop1': 'value1',
            'prop2': 'value2'
        })

    def test_set_method(self):
        entity = StubEntity(
            prop1="value1",
            prop2="value2"
        )

        entity._set("prop1", "some other value")

        self.assertEqual(entity.prop1, "some other value")
        