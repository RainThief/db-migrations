"""Seeder module"""
import os
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Callable, Any
from faker import Faker
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import MetaData, engine


class Seeder():
    """Abstract class to provide common seeding functionality

    Args:
        conn: SqlAlchemy connection
        operation: Migrations operation object
        meta: database schema

    Attributes:
        unique: Dict holding all values used to check uniqueness
        faker: Faker object to generate dummy data
    """

    __metaclass__ = ABCMeta

    unique: Dict[str, List[str]] = {}

    faker: Faker = Faker(['en_GB'])


    @abstractmethod
    def __init__(self, conn: engine.base.Connection):
        # set connection
        self.conn = conn

        # get operations context
        self.operation = Operations(MigrationContext.configure(conn))

        # get metadata from current connection
        self.meta = MetaData(bind=self.operation.get_bind())

        # reflect database
        self.meta.reflect()


    @staticmethod
    @abstractmethod
    def create_unique(unique_key: str, func: Callable[..., Any], *args: List[Any]):
        """Create a guaranteed unique value

        Args:
            unique_key: namespace to sanbox unique value generation
            func: call function to generate value
            args: optional args for callable function

        Returns:
            str: unique value
        """
        value = func(*args)

        # create unique key of not exists
        if unique_key not in Seeder.unique.keys():
            Seeder.unique[unique_key] = []

        # if value generated has already been used, recurse to try again
        if value in Seeder.unique[unique_key]:
            return Seeder.create_unique(unique_key, func, *args)

        Seeder.unique[unique_key].append(value)

        return value


    @abstractmethod
    def seed(self):
        """Runs seeder after checking env"""
        if os.getenv('SEED') != 'true':
            return
        self.run()


    @abstractmethod
    def run(self):
        """extend in child class to run seeding"""
