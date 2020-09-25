# pylint: skip-file

import unittest
import os
from unittest.mock import MagicMock
from unittest import mock
from .run_seeders import main
import scripts
from util.seeder import Seeder


# stop seeder connecting to database
def setUpModule():
    Seeder.connect = MagicMock()


class TestRunSeeder(unittest.TestCase):


    def test_will_seed_in_seed_env(self, *args):
        os.environ['SEED'] = "true"
        mock = scripts.run_seeders.run = MagicMock()
        main()
        mock.assert_called_once_with()


    def test_will_not_seed_in_non_seed_env(self, *args):
        os.environ['SEED'] = "false"
        mock = scripts.run_seeders.run = MagicMock()
        main()
        mock.assert_not_called()
