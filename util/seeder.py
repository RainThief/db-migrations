"""Seeder module"""
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Callable, Any
from faker import Faker
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import MetaData, sql, engine as eng, ext, orm
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


class NonUniqueError(Exception):
    """Non unique value exceptions"""


class TableError(Exception):
    """Table errors in DB"""


class Seeder():
    """Abstract class to provide common seeding functionality

    Attributes:
        _unique: Dict holding all values used to check uniqueness
        _engine: sqlalchemy engine
        _base: sqlalchemy base class for declaring models
        faker: Faker object to generate dummy data
        connection: sqlalchemy connection
        operation: sqlalchemy migration operations
        meta: database table schema meta
    """

    __metaclass__ = ABCMeta

    _unique: Dict[str, List[str]] = {}

    _engine: eng.Engine = None

    _base: ext.declarative.api.DeclarativeMeta = None

    faker: Faker = Faker(['en_GB'])

    connection: eng.base.Connection = None

    operation: Operations = None

    meta: sql.schema.MetaData = None


    @staticmethod
    def connect(engine: eng.Engine) -> None:
        """Instantiates an sqlalchemy connection shareable accross all seeders

        Args:
            engine: SqlAlchemy engine
        """

        #set engine
        Seeder._engine: engine.Engine = engine

        # set connection
        Seeder.connection = Seeder._engine.connect()

        # get operations context
        Seeder.operation = Operations(MigrationContext.configure(Seeder.connection))

        # get metadata from current connection
        Seeder.meta = MetaData(bind=Seeder.operation.get_bind())

        Seeder._base = automap_base()

        # reflect database
        Seeder._base.prepare(engine, reflect=True)
        Seeder.meta.reflect()


    @staticmethod
    def get_meta_model(table_name: str) -> ext.declarative.api.DeclarativeMeta:
        """Create model for given table name

        Args:
            table_name: namespace to sanbox unique value generation

        Returns:
            reflected model
        """
        try:
            return Seeder._base.classes[table_name]
        except KeyError as err:
            raise TableError(f"table {table_name} does not exist") from err


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
        try:
            if value in Seeder._unique[unique_key]:
                return Seeder.create_unique(unique_key, func, *args)
        except RecursionError as err:
            raise NonUniqueError("cannot generate unique value") from err

        Seeder._unique[unique_key].append(value)

        return value


    @staticmethod
    def create_session() -> orm.Session:
        """create a session for transactions"""
        # @todo test unique session
        return Session(Seeder._engine)


    @abstractmethod
    def _run(self) -> None:
        """extend in child class to run seeding"""
