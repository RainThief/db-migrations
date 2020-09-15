# pylint: skip-file

import unittest
import os
from unittest.mock import MagicMock
from .seeder import Seeder, NonUniqueError


class Counter():

    tick = 0

    @staticmethod
    def inc():
        Counter.tick += 1

    @staticmethod
    def reset():
        Counter.tick = 0



class TestSeeder(unittest.TestCase):


    def test_generates_unique_value(self):

        def unique_value():
            Counter.inc()
            if Counter.tick < 3:
                return 'not unique'
            return 'unique'

        first_value = Seeder.create_unique('test_pass', unique_value)
        second_value = Seeder.create_unique('test_pass', unique_value)

        self.assertNotEqual(
            first_value,
            second_value
        )
        Counter.reset()


    def test_impossible_unique_value_fails(self):
        with self.assertRaises(NonUniqueError):

            def non_unique_value():
                return 'not unique'

            first_value = Seeder.create_unique('test_pass', non_unique_value)
            second_value = Seeder.create_unique('test_pass', non_unique_value)

            self.assertNotEqual(
                first_value,
                second_value
            )


    def test_will_seed_in_seed_env(self):
        os.environ['SEED'] = "true"
        mock = Seeder._run = MagicMock()
        Seeder().seed()
        mock.assert_called_once_with()


    def test_will_not_seed_in_non_seed_env(self):
        os.environ['SEED'] = "false"
        mock = Seeder._run = MagicMock()
        Seeder().seed()
        mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
