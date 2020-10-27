"""database test lib wrapper"""


from typing import Union
from robot_support.database import SQLDatabase
from scripts import run_seeders
from util.seeder import Seeder


class DatabaseConnection:
    """Data class to hold connection state
    to avoid using globals which pylint hates"""

    SQLDatabase = None

    @staticmethod
    def set_url(db_url: str):
        """set db url connection string"""
        DatabaseConnection.SQLDatabase = SQLDatabase(db_url)


    @staticmethod
    def close():
        """clode db connection"""
        if DatabaseConnection.SQLDatabase is not None:
            DatabaseConnection.SQLDatabase.close_connection()


    @staticmethod
    def call(method: str, *args: Union[str, int]):
        """passthrough as magic method"""
        getattr(DatabaseConnection.SQLDatabase, method)(*args)



def check_column_names(table_name, expected_columns):
    """Checks a list of table column names

    Compares a list of table column names against an expect list

    Args:
        table_name: the table to query
        expected_records: the list of column names expected in table
    """
    DatabaseConnection.SQLDatabase.check_column_names(table_name, expected_columns.split(","))


def seed():
    """seed db"""
    Seeder.connect(DatabaseConnection.SQLDatabase.engine)
    run_seeders.run()
