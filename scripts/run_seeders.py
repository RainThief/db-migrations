"""script to run all seeders sequentially"""
import os
from alembic import config
import sqlalchemy as sa
from seeds.accounts_seeder import AccountsSeeder
from util.seeder import Seeder


def main() -> None:
    """
    Args:
        engine: SqlAlchemy engine
    """
    # list seeders here in order
    AccountsSeeder().run()


def get_engine() -> sa.engine.Engine:
    """instatiate and return an sqlalchemy connection

    Returns:
        sqlalchemy engine
    """
    return sa.engine.create_engine(
        config.Config('./alembic.ini').get_main_option('sqlalchemy.url')
    )


if __name__ == "__main__":
    if os.getenv('SEED') == 'true':
        Seeder.connect(get_engine())
        main()
