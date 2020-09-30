# pylint: skip-file
import unittest
import argparse
import sys
from unittest.mock import MagicMock
from pyfakefs.fake_filesystem_unittest import TestCase
from scripts.create_seeder import ValidateName, CreateSeeder, parse_args


validate: ValidateName


parser = argparse.ArgumentParser(
    prog='create_seeder.py',
    usage=None,
    description='create seeder module',
    formatter_class=argparse.HelpFormatter,
    conflict_handler='error',
    add_help=True
)


def setUpModule():
    global validate
    validate = ValidateName(
        ['--name'],
        'name',
        1,
        metavar='seeder class name',
        type=str,
        required=True
    )


class TestCreateSeeder(TestCase):


    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir('seeds')
        self.fs.create_file('migrations/seeder.py.mako')


    def test_accepts_valid_pascalcase_name_arg(self):
        validate(
            parser,
            CreateSeeder,
            ['TestSeeder'],
            '--name'
        )

        self.assertEqual(
            CreateSeeder.name,
            'TestSeeder'
        )

    def test_rejects_snakecase_name_arg(self):
        with self.assertRaises(ValueError):
            validate(
                parser,
                CreateSeeder,
                ['test_seeder'],
                '--name'
            )


    def test_rejects_camelcase_name_arg(self):
        with self.assertRaises(ValueError):
            validate(
                parser,
                CreateSeeder,
                ['testSeeder'],
                '--name'
            )


    def test_accepts_name_arg(self):
        sys.argv = [
            'scripts/create_seeder.py', '--name', 'TestSeeder'
        ]
        parse_args()
        self.assertEqual(
            CreateSeeder.name,
            'TestSeeder'
        )


    def test_fails_if_seeder_exists(self):
        with self.assertRaises(ValueError):
            self.fs.create_file('seeds/test_seeder.py')
            validate(
                parser,
                CreateSeeder,
                ['TestSeeder'],
                '--name'
            )


    def test_fails_if_missing_name_arg(self):
        with self.assertRaises(SystemExit) as exit_code:
            sys.argv = [
                'scripts/create_seeder.py', 'TestSeeder'
            ]
            parse_args()
            self.assertEqual(
                CreateSeeder.name,
                'TestSeeder'
            )
        self.assertEqual(exit_code.exception.code, 2)


    def test_fails_if_missing_extra_args(self):
        with self.assertRaises(SystemExit) as exit_code:
            sys.argv = [
                'scripts/create_seeder.py', '--name', 'TestSeeder', '--extra_arg'
            ]
            parse_args()
            self.assertEqual(
                CreateSeeder.name,
                'TestSeeder'
            )
        self.assertEqual(exit_code.exception.code, 2)


    def test_fails_cannot_write_file(self):
        sys.exit = MagicMock()
        self.fs.chmod('seeds', 0o000)
        sys.argv = [
            'scripts/create_seeder.py', '--name', 'TestSeeder'
        ]
        parse_args()
        self.assertRaises(PermissionError)
        self.assertEqual(exit_code.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
