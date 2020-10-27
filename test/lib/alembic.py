"""alembic library"""
from shutil import copyfile
from alembic import command
from alembic.util.exc import CommandError
from alembic.config import Config
from robot_support.logger import Logger


LOGGER = Logger.get_instance()


class AlembicError(Exception):
    """Log alembic error to file"""

    def __init__(self, value: str):
        super().__init__()
        LOGGER.error(f"Alembic error: {value}")


def migrate(direction: str, revision_id: str, db_url: str) -> None:
    """run alembic migrate command

    Args:
        direction: direction to migrate
        revision_id: revision to migrate to
    """
    copy_alembic_config()
    LOGGER.info("starting alembic migrate")

    cmd = command.upgrade
    if direction == "downgrade":
        cmd = command.downgrade

    try:
        cmd(init_alembic_config(db_url), revision_id)
    except CommandError as error:
        raise AlembicError(error) from error


def copy_alembic_config() -> None:
    """create alembic config file from template"""
    LOGGER.info("Creating alembic config file")
    copyfile('./migrations/alembic.ini-dist', './alembic.ini')
    cnf_file = open("./alembic.ini", "r")
    content = cnf_file.read()
    cnf_file.close()
    cnf_file = open("./alembic.ini", "w")
    cnf_file.write(content.replace('INFO', 'WARN'))
    cnf_file.close()


def init_alembic_config(db_url: str) -> Config:
    """init alembic config object"""
    config = Config('./alembic.ini')
    config.set_main_option("sqlalchemy.url", db_url)
    return config
