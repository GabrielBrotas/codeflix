import unittest
from dataclasses import is_dataclass
from _shared.domain.validators import ValidatorRules, ValidationException

class TestValidatorRulesUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValidatorRules(value="gabriel", prop="name")))

    def test_values_method(self):
        validator = ValidatorRules(value="gabriel", prop="name")
        self.assertEqual(validator.prop, "name")
        self.assertEqual(validator.value, "gabriel")

    def test_is_methods_return_instance(self):
        self.assertIsInstance(
            ValidatorRules.values("gabriel", "name").required(),
            ValidatorRules
        )

    def test_required_rule_single_error(self):
        invalid_datas = [
            {'value': None, 'prop': 'name'},
            {'value': "", 'prop': 'name'},
            {'value': "  ", 'prop': 'name'}
        ]

        for data in invalid_datas:
            error_log_msg=f'value: {data["value"]}, prop: {data["prop"]}'
            with self.assertRaises(ValidationException, msg=error_log_msg) as assert_error:
                value = data["value"] if data["value"] is None else str(data["value"]).strip()

                self.assertIsInstance(
                    ValidatorRules.values(value, data["prop"], throw_error=True).required(),
                    ValidatorRules
                )

            self.assertEqual(
                "The name is required",
                assert_error.exception.args[0],
            )

        valid_datas = [
            {'value': "gabriel", 'prop': 'name'},
            {'value': 5, 'prop': 'name'},
            {'value': 0, 'prop': 'name'},
            {'value': False, 'prop': 'name'},
            {'value': [], 'prop': 'name'},
            {'value': {}, 'prop': 'name'},
        ]

        for data in valid_datas:
            self.assertIsInstance(
                ValidatorRules.values(data["value"], data["prop"]).required(),
                ValidatorRules
            )

    def test_string_rule_single_error(self):
        invalid_datas = [
            {'value': 1, 'prop': 'name'},
            {'value': [], 'prop': 'name'},
            {'value': True, 'prop': 'name'},
            {'value': {}, 'prop': 'name'},
        ]

        for data in invalid_datas:
            error_log_msg=f'value: {data["value"]}, prop: {data["prop"]}'
            with self.assertRaises(ValidationException, msg=error_log_msg) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.values(data["value"], data["prop"], throw_error=True).string(),
                    ValidatorRules
                )

            self.assertEqual(
                "The name must be a string",
                assert_error.exception.args[0],
            )

        valid_datas = [
            {'value': "gabriel", 'prop': 'name'},
            {'value': "", 'prop': 'name'},
            {'value': None, 'prop': 'name'},
        ]

        for data in valid_datas:
            self.assertIsInstance(
                ValidatorRules.values(data["value"], data["prop"]).string(),
                ValidatorRules
            )

    def test_max_length_rule_single_error(self):
        # lets assume the max length is 5
        invalid_datas = [
            {'value': "t" * 6, 'prop': 'name'},
        ]

        for data in invalid_datas:
            error_log_msg=f'value: {data["value"]}, prop: {data["prop"]}'
            with self.assertRaises(ValidationException, msg=error_log_msg) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.values(data["value"], data["prop"], throw_error=True).max_length(5),
                    ValidatorRules
                )

            self.assertEqual(
                "The name length must be smaller than 5",
                assert_error.exception.args[0],
            )

        valid_datas = [
            {'value': "t" * 1, 'prop': 'name'},
            {'value': "t" * 2, 'prop': 'name'},
            {'value': "t" * 3, 'prop': 'name'},
            {'value': "t" * 4, 'prop': 'name'},
            {'value': "t" * 5, 'prop': 'name'},
            {'value': "", 'prop': 'name'},
            {'value': None, 'prop': 'name'},
        ]

        for data in valid_datas:
            self.assertIsInstance(
                ValidatorRules.values(data["value"], data["prop"]).string(),
                ValidatorRules
            )

    def test_boolean_rule_single_error(self):
        invalid_datas = [
            {'value': "t", 'prop': 'name'},
            {'value': 5, 'prop': 'name'},
            {'value': {}, 'prop': 'name'},
            {'value': [], 'prop': 'name'},
        ]

        for data in invalid_datas:
            error_log_msg=f'value: {data["value"]}, prop: {data["prop"]}'
            with self.assertRaises(ValidationException, msg=error_log_msg) as assert_error:
                self.assertIsInstance(
                    ValidatorRules.values(data["value"], data["prop"], throw_error=True).boolean(),
                    ValidatorRules
                )

            self.assertEqual(
                "The name must be boolean",
                assert_error.exception.args[0],
            )

        valid_datas = [
            {'value': True, 'prop': 'name'},
            {'value': False, 'prop': 'name'},
            {'value': None, 'prop': 'name'},
        ]

        for data in valid_datas:
            self.assertIsInstance(
                ValidatorRules.values(data["value"], data["prop"]).boolean(),
                ValidatorRules
            )

    def test_composed_rules(self):
        with self.assertRaises(ValidationException) as assert_error:
            self.assertIsInstance(
                ValidatorRules.values(1, "prop", throw_error=True)
                    .required().string().max_length(5),
                ValidatorRules
            )

        self.assertEqual(
            "The prop must be a string",
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.assertIsInstance(
                ValidatorRules.values("t"*6, "prop", throw_error=True)
                    .required().string().max_length(5),
                ValidatorRules
            )

        self.assertEqual(
            "The prop length must be smaller than 5",
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            self.assertIsInstance(
                ValidatorRules.values(6, "prop", throw_error=True).required().boolean(),
                ValidatorRules
            )

        self.assertEqual(
            "The prop must be boolean",
            assert_error.exception.args[0],
        )

    def test_rules_without_throw_error(self):
        ValidatorRules.values(1, "prop").required().string().max_length(5)
        ValidatorRules.values("t" * 6, "prop2").string().max_length(5)
        validator = ValidatorRules.values([], "prop3").required().boolean()
        self.assertIsInstance(validator, ValidatorRules)
