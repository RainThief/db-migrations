"""script to run all seeders sequentially"""
from alembic import config
import sqlalchemy as sa
from seeds.accounts_seeder import AccountsSeeder


def main(connection: sa.engine.base.Connection):
    """
    Args:
        conn: SqlAlchemy connection
    """
    # list seeders here in order
    AccountsSeeder(connection).run()


def get_connection():
    """instatiate and return an sqlalchemy connection

    Returns:
        sa.engine.base.Connection: unique value
    """
    alembic_cfg = config.Config("./alembic.ini")
    engine = sa.engine.create_engine(alembic_cfg.get_main_option('sqlalchemy.url'))
    return engine.connect()


if __name__ == "__main__":
    main(get_connection())
