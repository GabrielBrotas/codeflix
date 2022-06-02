
import unittest

from _shared.domain.notification import Notification

ERROR_MSG_1 = 'error 1'
ERROR_MSG_2 = 'error 2'
class TestNotificationUnit(unittest.TestCase):

    def test_if_can_add_errors(self):
        notifications = Notification()

        self.assertDictEqual(notifications.get_errors(), {})

        notifications.add_error('prop1', ERROR_MSG_1)

        self.assertDictEqual(notifications.get_errors(), {
            'prop1': [ERROR_MSG_1]
        })

        notifications.add_error('prop1', ERROR_MSG_2)

        self.assertDictEqual(notifications.get_errors(), {
            'prop1': [ERROR_MSG_1, ERROR_MSG_2]
        })

    def test_if_has_errors(self):
        notifications = Notification()
        self.assertFalse(notifications.has_errors())

        notifications.add_error('prop1', ERROR_MSG_1)
        self.assertTrue(notifications.has_errors())

        notifications.add_error('prop1', ERROR_MSG_2)
        self.assertTrue(notifications.has_errors())

    def test_get_errors_message(self):
        notifications = Notification()
        self.assertEqual(notifications.get_errors_msg(), "")

        notifications.add_error('prop1', ERROR_MSG_1)
        notifications.add_error('prop1', ERROR_MSG_2)
        notifications.add_error('prop2', ERROR_MSG_2)

        expected_error_msg = f'prop1:{ERROR_MSG_1},{ERROR_MSG_2};prop2:{ERROR_MSG_2};'

        self.assertEqual(notifications.get_errors_msg(), expected_error_msg)
