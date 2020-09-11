"""Seeder module"""
import os
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Callable, Any
from faker import Faker
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import MetaData, sql, engine, ext, orm
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class Seeder():
    """Abstract class to provide common seeding functionality

    Args:
        eng: SqlAlchemy engine

    Attributes:
        _unique: Dict holding all values used to check uniqueness
        faker: Faker object to generate dummy data
        connection: sqlalchemy connection
        operation: sqlalchemy migration operations
        meta: database table schema meta
        base: sqlalchemy base class for declaring models
        engine: sqlalchemy engine
    """

    __metaclass__ = ABCMeta

    _unique: Dict[str, List[str]] = {}

    faker: Faker = Faker(['en_GB'])

    connection: engine.base.Connection = None

    operation: Operations = None

    meta: sql.schema.MetaData = None

    base: ext.declarative.api.DeclarativeMeta = None




    def __init__(self, eng: engine.Engine) -> None:

        self.engine: engine.Engine = eng

        # set connection
        Seeder.connection = eng.connect()

        # get operations context
        Seeder.operation = Operations(MigrationContext.configure(Seeder.connection))

        # get metadata from current connection
        Seeder.meta = MetaData(bind=self.operation.get_bind())

        Seeder.base = automap_base()

        # reflect database
        Seeder.base.prepare(eng, reflect=True)
        Seeder.meta.reflect()


    @staticmethod
    def create_unique(unique_key: str, func: Callable[..., Any], *args: List[Any]) -> str:
        """Create a guaranteed unique value

        Args:
            unique_key: namespace to sanbox unique value generation
            func: call function to generate value
            args: optional args for callable function

        Returns:
            unique value
        """
        value: Callable[..., Any] = func(*args)

        # create unique key of not exists
        if unique_key not in Seeder._unique.keys():
            Seeder._unique[unique_key] = []

        # if value generated has already been used, recurse to try again
        if value in Seeder._unique[unique_key]:
            return Seeder.create_unique(unique_key, func, *args)

        Seeder._unique[unique_key].append(value)

        return value


    def create_session(self) -> orm.Session:
        """create a session for transactions"""
        return Session(self.engine)


    def seed(self) -> None:
        """Runs seeder after checking env"""
        if os.getenv('SEED') != 'true':
            return
        self.run()


    @abstractmethod
    def run(self) -> None:
        """extend in child class to run seeding"""
