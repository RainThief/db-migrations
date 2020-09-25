"""create seeder script"""
import argparse
import os
import sys
from typing import List
from inflection import camelize, underscore
from mako.template import Template


BASE_PATH: str = "./seeds"


class CreateSeeder:
    """Creates a new seeder file class from mako template

    Attributes:
        name: seeder class name in PascalCase
    """


    name: str


    @staticmethod
    def create_file():
        """Creates seeder file after checking file does not exist"""
        seeder_file_path = f"{BASE_PATH}/{underscore(CreateSeeder.name)}.py"
        seeder_file = open(seeder_file_path,"w+")
        seeder_file.write(
            Template(filename='./migrations/seeder.py.mako') \
                .render(
                    seeder_name=CreateSeeder.name,
                    message=f"{CreateSeeder.name} seeder module"
                )
        )
        seeder_file.close()
        print(f"{seeder_file_path} created")



class ValidateName(argparse.Action):
    """Validates argparse values"""


    def __call__(
        self, parser: argparse.ArgumentParser, namespace: type, values: List[str], option_string: str = None
    ) -> None:
        """Validates args passed to script

        Args:
            parser: argparse.ArgumentParser object
            namespace: object to pass arg values into attributes
            values: List of values parsed from args
            option_string: list of flags in args
        """
        value = values[0]

        if camelize(value, True) != value:
            raise ValidateName.raise_error("seeder names must be in PascalCase")

        if os.path.exists(f"{BASE_PATH}/{underscore(value)}.py"):
            raise ValidateName.raise_error(f"seeder {value} already exists")

        setattr(namespace, self.dest, values[0])


    @staticmethod
    def raise_error(msg: str) -> ValueError:
        """Raise value error with given message"""
        return ValueError(f"{os.path.basename(__file__)} error: {msg}")



def parse_args():
    """Parse script args using argparse"""
    parser = argparse.ArgumentParser(description='create seeder module')
    parser.add_argument('--name', metavar='seeder class name', **{
        "type": str,
        "nargs": 1,
        "action": ValidateName,
        "required": True
    })
    try:
        parser.parse_args(None, namespace=CreateSeeder)
        CreateSeeder.create_file()
    except (ValueError, PermissionError) as err:
        print(err, file=sys.stderr)
        sys.exit(1)



if __name__ == "__main__":
    parse_args()
