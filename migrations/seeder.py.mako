# this import may not be used if not using sqlalchemy imports
# but needs to be in template for convienece
"""${message}"""
import sqlalchemy as sa # pylint: disable=unused-import
from util.seeder import Seeder

# we can allow for `self` to be used as instantiated class
# incase seeder needs to hold state datạ
# pylint: disable=no-self-use


class ${seeder_name}(Seeder):
    """seeder class"""


    def run(self) -> None:
        """run seeding logic"""
